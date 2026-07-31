<div align="center">
  <h1>⚡️ Snag</h1>
  <p><strong>A premium, lightweight, frameless floating macOS widget for rapid access to your transient files and text.</strong></p>
  
  [![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)]()
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
  [![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)]()
  [![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)]()
</div>

---

## 🌟 The Vision

**Snag** lives quietly in the bottom right corner of your screen, appearing instantly with a global keyboard shortcut. Designed to be ultra-premium with a matte dark mode, charcoal grey background, and subtle noise texture overlay. No clutter, just the files and text you need right now.

## ✨ Key Features

- 🖼️ **Screenshots Hub**: Instantly access your 10 most recent screenshots from `~/Desktop` and `~/Pictures/Screenshots`.
- 📥 **Downloads Tracker**: See your 10 latest downloaded files in real-time.
- 📋 **Clipboard Manager**: A rolling history of your last 15 copied text snippets.
- 📌 **Pinned Snippets**: Save and quickly retrieve custom text blocks.
- 🖐️ **Seamless Drag & Drop**: Drag files and text directly out of the widget into any other macOS app (Finder, Chrome, Slack, etc.).

## 🛠 Tech Stack

- **Desktop Client:** Python 3 + PyQt6 (Packaged natively via PyInstaller)
- **Web & Backend:** Next.js 14 (App Router) hosted on Vercel
- **Database:** Supabase (PostgreSQL)
- **Payments:** Razorpay & PayPal via Webhooks

## 🚀 Installation (macOS)

You can install Snag directly via your terminal. Our custom script downloads the latest release, installs it to `/Applications`, bypasses Gatekeeper restrictions safely, and launches it immediately.

```bash
curl -fsSL https://[YOUR_DOMAIN].com/install.sh | bash
```

Alternatively, you can build from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/Aryan-Protein-Vala/Snag.git
   cd Snag/desktop
   ```
2. Install dependencies:
   ```bash
   pip install PyQt6 pynput watchdog pyinstaller
   ```
3. Build the macOS App:
   ```bash
   pyinstaller --windowed --name Snag main.py
   ```
4. Move to Applications:
   ```bash
   cp -R dist/Snag.app /Applications/
   ```

## 🔒 Licensing & Activation

On first launch, Snag binds securely to your macOS Hardware UUID.
1. Enter your 16-character license key.
2. The app communicates with our Next.js backend to validate and activate your machine.

---
<div align="center">
  <i>Built with ❤️ for macOS power users.</i>
</div>
