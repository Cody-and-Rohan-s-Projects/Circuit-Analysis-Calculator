#!/bin/bash

# Define paths
APPDIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_FILE_NAME="CircuitAnalysis.desktop"
ICON_SRC="$APPDIR/_internal/icon.png"
ICON_NAME="circuitanalysis.png"
ICON_DEST="$HOME/.local/share/icons/$ICON_NAME"
DESKTOP_DEST="$HOME/.local/share/applications/$DESKTOP_FILE_NAME"

echo "🔧 Installing Circuit Analysis..."

# Copy icon to icon directory
mkdir -p "$HOME/.local/share/icons"
cp "$ICON_SRC" "$ICON_DEST"

# Create .desktop file with absolute paths
cat > "$DESKTOP_DEST" <<EOF
[Desktop Entry]
Name=Circuit Analysis
Comment=AC/DC Circuit Solver
Exec=$APPDIR/CircuitAnalysis
Icon=$ICON_DEST
Type=Application
Terminal=false
Categories=Utility;
EOF

# Make files executable
chmod +x "$APPDIR/CircuitAnalysis"
chmod +x "$DESKTOP_DEST"

# Refresh desktop database
update-desktop-database "$HOME/.local/share/applications"

echo "✅ Installed! You can now find 'Circuit Analysis' in your app menu."

zenity --info --title="Circuit Analysis Installer" --text="✅ Installation complete!\n\nYou can now find 'Circuit Analysis' in your app menu."




