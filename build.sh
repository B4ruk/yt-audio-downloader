#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

case "$(uname -s)" in
  Linux*)  ICON=assets/icon.png;  MODE=--onefile ;;
  Darwin*) ICON=assets/icon.icns; MODE=--onedir ;;
  *)       ICON=assets/icon.ico;  MODE=--onedir ;;
esac

pyinstaller --noconfirm --clean \
  "$MODE" --windowed \
  --name "YT-Audio-Downloader" \
  --icon "$ICON" \
  --osx-bundle-identifier io.github.b4ruk.ytaudiodownloader \
  --collect-data imageio_ffmpeg \
  --collect-data yt_dlp \
  --hidden-import PIL._tkinter_finder \
  youtube_downloader.py
