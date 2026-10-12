#!/usr/bin/env bash
rm -f "$HOME/.local/bin/yt-audio-downloader" \
      "$HOME/.local/share/icons/hicolor/256x256/apps/yt-audio-downloader.png" \
      "$HOME/.local/share/applications/yt-audio-downloader.desktop"
command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications" || true
echo "✓ YT Audio Downloader removido."
