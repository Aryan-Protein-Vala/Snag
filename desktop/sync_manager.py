import os
import time
from PyQt6.QtCore import QThread, pyqtSignal

try:
    from supabase import create_client, Client
except ImportError:
    pass

class SyncManager(QThread):
    new_clipboard = pyqtSignal(str)
    new_snippet = pyqtSignal(str)

    def __init__(self, sync_key: str):
        super().__init__()
        self.sync_key = sync_key
        self.running = True
        
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")
        
        # Fallback to local config file
        if not self.url or not self.key:
            import json
            config_path = os.path.expanduser("~/.config/snag/config.json")
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as f:
                        cfg = json.load(f)
                        self.url = cfg.get("SUPABASE_URL", self.url)
                        self.key = cfg.get("SUPABASE_KEY", self.key)
                except: pass
        self.client = None
        self.last_seen_ids = set()
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
            except Exception as e:
                print("Failed to init Supabase:", e)

    def push_clipboard(self, content: str):
        if not self.client: return
        try:
            self.client.table("snag_sync").insert({
                "sync_key": self.sync_key,
                "type": "clipboard",
                "content": content
            }).execute()
        except Exception as e:
            print("Push clipboard failed:", e)

    def push_snippet(self, content: str):
        if not self.client: return
        try:
            self.client.table("snag_sync").insert({
                "sync_key": self.sync_key,
                "type": "snippet",
                "content": content
            }).execute()
        except Exception as e:
            print("Push snippet failed:", e)

    def run(self):
        if not self.client:
            print("SyncManager: No SUPABASE_URL or SUPABASE_KEY provided. Cloud Sync disabled.")
            return

        print("SyncManager: Connected to Supabase. Listening for cloud clipboard/snippets...")
        # Populate initial seen IDs so we don't pull our own old history on boot
        try:
            resp = self.client.table("snag_sync").select("id").eq("sync_key", self.sync_key).order("created_at", desc=True).limit(20).execute()
            for row in resp.data:
                self.last_seen_ids.add(row["id"])
        except: pass

        while self.running:
            try:
                response = self.client.table("snag_sync").select("*").eq("sync_key", self.sync_key).order("created_at", desc=True).limit(5).execute()
                for row in reversed(response.data):
                    row_id = row.get("id")
                    if row_id not in self.last_seen_ids:
                        self.last_seen_ids.add(row_id)
                        
                        item_type = row.get("type")
                        content = row.get("content")
                        
                        if item_type == "clipboard":
                            self.new_clipboard.emit(content)
                        elif item_type == "snippet":
                            self.new_snippet.emit(content)
            except Exception as e:
                pass # Silent fail on poll
                
            time.sleep(4)

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
