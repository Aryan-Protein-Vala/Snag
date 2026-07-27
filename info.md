# Project Overview: Snag (macOS Productivity Widget)

## 1. Core Concept
"Snag" is a premium, lightweight, frameless floating macOS widget designed for rapid access to transient files and text. It opens via a global keyboard shortcut, appearing consistently in the bottom right corner of the screen. 

## 2. Tech Stack
- **Desktop Client:** Python 3 + PyQt6 (packaged with PyInstaller).
- **Web/Backend:** Next.js 14 (App Router) hosted on Vercel.
- **Database:** Supabase (PostgreSQL).
- **Payments:** Razorpay (INR) and PayPal (USD) via API webhooks.
- **Distribution:** Hosted `.zip` file installed via a custom Shell script to bypass macOS Gatekeeper.

## 3. Desktop Client (PyQt6) Specifications

### UI / UX Design
- **Window:** `Qt.WindowType.FramelessWindowHint` and `Qt.WindowType.WindowStaysOnTopHint`.
- **Dimensions:** Fixed size ~340x480px. Appears at the bottom right.
- **Theme:** Ultra-premium, matte dark mode. Background is charcoal grey (`#1A1A1A`) with a simulated subtle noise/grain texture overlay. 
- **Borders:** 12px rounded corners. 
- **Typography:** SF Pro (macOS native), with white/light-grey titles (`#E0E0E0`) and dimmed timestamps/subtitles (`#808080`). No bright multi-colors.
- **Interactions:** List items highlight to `#333333` on hover. All items in the lists must be draggable directly out of the widget into other macOS apps (Finder, Chrome, Slack) using `QDrag`.

### The 4 Tabs (Segmented Header)
The header contains 4 monochromatic vector line icons (Outline style):
1. **Screenshots (Frame Icon):** Uses `watchdog` to monitor `~/Desktop` and `~/Pictures/Screenshots`. Shows the 10 most recent images.
2. **Downloads (Down Arrow Icon):** Uses `watchdog` to monitor `~/Downloads`. Shows the 10 most recent files.
3. **Copied Text (Clipboard Icon):** Uses `pyperclip` (or PyQt's native `QClipboard`) to maintain a rolling history of the last 15 copied text strings.
4. **Pinned Text (Pushpin Icon):** Reads/writes custom user snippets to `~/.config/snag/snippets.json`. Includes a discrete `+` button in the UI to add new text blocks.

### Licensing & Hardware Lock
- On first launch, the app checks `~/.config/snag/license.json`.
- If missing/invalid, a centered activation UI blocks the app, requesting a 16-character license key.
- The app fetches the macOS Hardware UUID (e.g., via `ioreg -rd1 -c IOPlatformExpertDevice`).
- Makes a `POST` request to `https://[YOUR_DOMAIN].com/api/activate` with `{ key, device_id }`.

---

## 4. Web & Backend Specifications (Next.js App Router)

### Landing Page
- A sleek, dark-themed one-pager explaining the tool.
- Pricing uses the Decoy Effect: Monthly ($0.99/₹29), Yearly ($3.99/₹199), and Lifetime ($14.99/₹899).

### Database Schema (Supabase)
Table: `licenses`
- `id` (uuid, pk)
- `license_key` (varchar 19, unique) - Format: `SNAG-XXXX-XXXX-XXXX`
- `plan_type` (varchar) - 'monthly', 'yearly', 'lifetime'
- `is_active` (boolean) - default false
- `device_id` (varchar) - nullable (stores the Mac Hardware UUID)
- `expires_at` (timestamp) - nullable (for monthly/yearly)
- `created_at` (timestamp)

### API Routes
1. **`/api/webhooks/payment`**: Listens for Razorpay/PayPal successful payment hooks. Generates the 16-character key, saves to Supabase, and emails it via Resend.
2. **`/api/activate`**: Accepts the key and `device_id`. 
   - If `device_id` is null in DB, saves the incoming ID and activates.
   - If `device_id` matches, returns success (200).
   - If `device_id` differs, returns error 403 (Device mismatch).

### The Installer Route
1. **`/install.sh/route.ts`**: This Next.js route handler serves a raw Bash script (MIME type: `text/plain`). 
2. Users run `curl -fsSL https://[YOUR_DOMAIN].com/install.sh | bash` in their terminal.
3. The script:
   - Downloads `Snag.zip`.
   - Unzips it to `/Applications/Snag.app`.
   - Runs `xattr -cr /Applications/Snag.app` (Crucial: Wipes the Apple Gatekeeper quarantine flag).
   - Runs `open /Applications/Snag.app` to launch it instantly for the user.

## 5. Development Phases
1. **Phase 1:** Build the PyQt6 UI frame and tabs (Mock data).
2. **Phase 2:** Wire up OS watchers (Downloads, Screenshots, Clipboard, Drag-and-Drop).
3. **Phase 3:** Build the Next.js site, Supabase table, and `install.sh` script.
4. **Phase 4:** Connect the Payment webhooks and PyQt6 licensing gate.