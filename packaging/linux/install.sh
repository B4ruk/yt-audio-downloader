#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
APP_DIR="$HOME/.local/share/applications"

mkdir -p "$BIN_DIR" "$ICON_DIR" "$APP_DIR"
install -m 755 YT-Audio-Downloader "$BIN_DIR/yt-audio-downloader"
install -m 644 icon.png "$ICON_DIR/yt-audio-downloader.png"

cat > "$APP_DIR/yt-audio-downloader.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=YT Audio Downloader
Comment=Baixe o áudio de vídeos do YouTube
Exec=$BIN_DIR/yt-audio-downloader
Icon=yt-audio-downloader
Terminal=false
Categories=AudioVideo;Audio;Network;
DESKTOP

command -v update-desktop-database >/dev/null && update-desktop-database "$APP_DIR" || true
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q "$HOME/.local/share/icons/hicolor" 2>/dev/null || true

echo "✓ Instalado. Procure por \"YT Audio Downloader\" no menu de aplicativos"
echo "  ou execute: yt-audio-downloader"
