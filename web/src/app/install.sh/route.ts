import { NextResponse } from 'next/server';

const scriptContent = `#!/bin/bash
echo "====================================="
echo "        INSTALLING SNAG WIDGET       "
echo "====================================="

OS="$(uname -s)"
ARCH="$(uname -m)"

echo "Detected OS: $OS"

if [ "$OS" = "Darwin" ]; then
    echo "Downloading Snag for macOS..."
    curl -fsSL https://example.com/app-release-mac.zip -o /tmp/Snag.zip
    echo "Extracting to /Applications..."
    unzip -oq /tmp/Snag.zip -d /Applications/
    echo "Removing Gatekeeper quarantine..."
    xattr -cr /Applications/Snag.app
    echo "Launching Snag..."
    open /Applications/Snag.app
    rm /tmp/Snag.zip
    echo "Done!"
elif [ "$OS" = "Linux" ]; then
    echo "Downloading Snag for Linux..."
    curl -fsSL https://example.com/app-release-linux.zip -o /tmp/Snag.zip
    echo "Extracting to ~/.local/bin/..."
    mkdir -p ~/.local/bin
    unzip -oq /tmp/Snag.zip -d ~/.local/bin/
    chmod +x ~/.local/bin/snag
    echo "Launching Snag..."
    ~/.local/bin/snag &
    rm /tmp/Snag.zip
    echo "Done!"
elif [ "$(expr substr $OS 1 5)" = "MINGW" ] || [ "$(expr substr $OS 1 4)" = "MSYS" ]; then
    echo "Downloading Snag for Windows..."
    curl -fsSL https://example.com/app-release-win.zip -o /tmp/Snag.zip
    echo "Extracting..."
    mkdir -p ~/AppData/Local/Snag
    unzip -oq /tmp/Snag.zip -d ~/AppData/Local/Snag/
    echo "Done. Launch Snag from your start menu or ~/AppData/Local/Snag."
else
    echo "Unsupported OS: $OS"
    exit 1
fi
`;

export async function GET() {
  return new NextResponse(scriptContent, {
    headers: {
      'Content-Type': 'text/plain',
    },
  });
}
