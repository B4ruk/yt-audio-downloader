# YT Audio Downloader

<p align="center"><img src="assets/icon.png" width="96" alt="ícone"></p>

Aplicativo desktop para baixar o áudio de vídeos do YouTube e converter para **MP3, AAC, FLAC, WAV ou M4A**. Interface gráfica simples, tema escuro, e o FFmpeg já vem embutido — não precisa instalar nada além do executável.

## Download

Baixe a versão mais recente na página de [Releases](../../releases/latest) ou no [SourceForge](https://sourceforge.net/projects/yt-audio-downloader/files/). Não é preciso ter Python instalado.

| Sistema | Arquivo |
|---|---|
| Windows | `…-windows-x64-setup.exe` (instalador) ou `…-windows-x64-portable.zip` |
| Linux (x86_64) | `…-linux-x86_64.zip` |
| macOS (Apple Silicon) | `…-macos-arm64.zip` |

O passo a passo de cada sistema está em **[INSTALL.md](INSTALL.md)**.

## Funcionalidades

- Colar a URL do vídeo e baixar com um clique
- Escolha de formato (MP3, AAC, FLAC, WAV, M4A) e qualidade
- Suporte a playlists com seleção de faixas
- Barra de progresso em tempo real
- FFmpeg embutido via `imageio-ffmpeg`

## Rodando a partir do código-fonte

Requer Python 3.10+ com `tkinter` (no Debian/Ubuntu: `sudo apt install python3-tk`).

```bash
git clone https://github.com/B4ruk/yt-audio-downloader.git
cd yt-audio-downloader
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python youtube_downloader.py
```

## Gerando o executável

```bash
pip install -r requirements-dev.txt
./build.sh
# saída em dist/
```

Os pacotes das releases (instalador Windows via [Inno Setup](https://jrsoftware.org/isinfo.php), ZIPs de Linux/macOS) são gerados automaticamente pelo GitHub Actions ao publicar uma tag `v*` (ex.: `git tag v1.0.0 && git push --tags`).

## Aviso legal

Este projeto é apenas uma interface para o [yt-dlp](https://github.com/yt-dlp/yt-dlp). Use-o somente para baixar conteúdo do qual você tenha direitos ou permissão, respeitando os [Termos de Serviço do YouTube](https://www.youtube.com/t/terms) e as leis de direitos autorais do seu país. O autor não se responsabiliza pelo uso indevido.

## Licença

[MIT](LICENSE)

O executável distribuído inclui o FFmpeg (licença LGPL/GPL), o yt-dlp (Unlicense) e o Pillow (MIT-CMU), cada um sob sua própria licença.
