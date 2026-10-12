"""
YouTube Audio Downloader
Requisitos: pip install -r requirements.txt
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import threading
import os
import sys

try:
    import yt_dlp
except ImportError:
    print("yt-dlp não encontrado. Instale com: pip install -r requirements.txt")
    sys.exit(1)

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None


class _SilentLogger:
    def debug(self, _): pass
    def info(self, _): pass
    def warning(self, _): pass
    def error(self, _): pass


def _build_icon():
    try:
        from PIL import Image, ImageDraw, ImageTk
        size = 64
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Fundo circular vermelho
        draw.ellipse([0, 0, size - 1, size - 1], fill=(255, 68, 68, 255))

        # Seta de download (branca)
        # Haste vertical
        draw.rectangle([28, 12, 36, 36], fill=(255, 255, 255, 255))
        # Cabeça da seta (triângulo)
        draw.polygon([(16, 34), (48, 34), (32, 50)], fill=(255, 255, 255, 255))
        # Barra base
        draw.rectangle([14, 52, 50, 58], fill=(255, 255, 255, 255))

        return ImageTk.PhotoImage(img)
    except Exception:
        return None


# ── Cores e estilo ────────────────────────────────────────────────────────────
BG        = "#0f0f0f"
SURFACE   = "#1a1a1a"
BORDER    = "#2a2a2a"
ACCENT    = "#ff4444"
ACCENT2   = "#ff6b35"
TEXT      = "#f0f0f0"
TEXT_DIM  = "#888888"
SUCCESS   = "#44ff88"
ERROR     = "#ff4444"


class YoutubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YT Audio Downloader")
        self.geometry("620x500")
        self.resizable(False, False)
        self.configure(bg=BG)

        icon = _build_icon()
        if icon:
            self.iconphoto(True, icon)
            self._icon = icon  # evita garbage collection

        self.output_dir = next(
            (p for p in map(os.path.expanduser, ("~/Músicas", "~/Music")) if os.path.isdir(p)),
            os.path.expanduser("~"),
        )
        self.is_downloading = False
        self._track_info = {"index": 0, "total": 1}

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, height=4)
        header.pack(fill="x")

        title_frame = tk.Frame(self, bg=BG, pady=20)
        title_frame.pack(fill="x", padx=30)

        tk.Label(title_frame, text="YouTube Audio Downloader",
                 font=("Courier New", 18, "bold"),
                 fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(title_frame, text="Baixe o áudio de qualquer vídeo do YouTube em MP3",
                 font=("Courier New", 10),
                 fg=TEXT_DIM, bg=BG).pack(anchor="w")

        # Separador
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=30)

        # URL
        self._section("URL do Vídeo", pady_top=20)
        url_frame = tk.Frame(self, bg=BG, padx=30)
        url_frame.pack(fill="x")

        self.url_var = tk.StringVar()
        url_entry = tk.Entry(
            url_frame, textvariable=self.url_var,
            font=("Courier New", 11), fg=TEXT, bg=SURFACE,
            insertbackground=ACCENT, relief="flat",
            bd=0, highlightthickness=1,
            highlightcolor=ACCENT, highlightbackground=BORDER
        )
        url_entry.pack(fill="x", ipady=10, ipadx=10)

        btn_paste = tk.Button(
            url_frame, text="📋 Colar da área de transferência",
            font=("Courier New", 9), fg=TEXT_DIM, bg=BG,
            relief="flat", bd=0, cursor="hand2",
            activeforeground=ACCENT, activebackground=BG,
            command=self._paste_url
        )
        btn_paste.pack(anchor="w", pady=(4, 0))

        # Formato
        self._section("Formato de Áudio", pady_top=16)
        fmt_frame = tk.Frame(self, bg=BG, padx=30)
        fmt_frame.pack(fill="x")

        self.format_var = tk.StringVar(value="mp3")
        formats = [("MP3", "mp3"), ("AAC", "aac"), ("FLAC", "flac"), ("WAV", "wav"), ("M4A", "m4a")]
        for label, val in formats:
            rb = tk.Radiobutton(
                fmt_frame, text=label, variable=self.format_var, value=val,
                font=("Courier New", 10), fg=TEXT, bg=BG,
                selectcolor=SURFACE, activebackground=BG, activeforeground=ACCENT,
                indicatoron=True, relief="flat", cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 16))

        # Qualidade
        self._section("Qualidade", pady_top=16)
        q_frame = tk.Frame(self, bg=BG, padx=30)
        q_frame.pack(fill="x")

        self.quality_var = tk.StringVar(value="192")
        qualities = [("128 kbps", "128"), ("192 kbps", "192"), ("256 kbps", "256"), ("320 kbps", "320")]
        for label, val in qualities:
            rb = tk.Radiobutton(
                q_frame, text=label, variable=self.quality_var, value=val,
                font=("Courier New", 10), fg=TEXT, bg=BG,
                selectcolor=SURFACE, activebackground=BG, activeforeground=ACCENT,
                indicatoron=True, relief="flat", cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 16))

        # Pasta de saída
        self._section("Pasta de Destino", pady_top=16)
        dir_frame = tk.Frame(self, bg=BG, padx=30)
        dir_frame.pack(fill="x")

        self.dir_label = tk.Label(
            dir_frame, text=self.output_dir,
            font=("Courier New", 9), fg=TEXT_DIM, bg=SURFACE,
            anchor="w", padx=10, pady=6
        )
        self.dir_label.pack(side="left", fill="x", expand=True)

        tk.Button(
            dir_frame, text="📁 Alterar",
            font=("Courier New", 9), fg=TEXT, bg=BORDER,
            relief="flat", bd=0, cursor="hand2", padx=10,
            activeforeground=ACCENT, activebackground=BORDER,
            command=self._choose_dir
        ).pack(side="left", padx=(8, 0), ipady=6)

        # Botão principal
        btn_frame = tk.Frame(self, bg=BG, pady=20, padx=30)
        btn_frame.pack(fill="x")

        self.btn_download = tk.Button(
            btn_frame, text="⬇  BAIXAR ÁUDIO",
            font=("Courier New", 13, "bold"),
            fg=BG, bg=ACCENT,
            relief="flat", bd=0, cursor="hand2",
            activeforeground=BG, activebackground=ACCENT2,
            command=self._start_download
        )
        self.btn_download.pack(fill="x", ipady=12)

        # Status / log
        self.status_var = tk.StringVar(value="Aguardando URL...")
        self.status_label = tk.Label(
            self, textvariable=self.status_var,
            font=("Courier New", 10), fg=TEXT_DIM, bg=BG
        )
        self.status_label.pack(pady=(0, 6))

        self.progress = ttk.Progressbar(self, mode="indeterminate", length=560)
        self.progress.pack(padx=30)

        # Estilo da barra de progresso
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TProgressbar", troughcolor=SURFACE, background=ACCENT, thickness=4)

    def _section(self, text, pady_top=10):
        lbl = tk.Label(self, text=text.upper(),
                       font=("Courier New", 8, "bold"),
                       fg=ACCENT, bg=BG)
        lbl.pack(anchor="w", padx=30, pady=(pady_top, 4))

    # ── Ações ─────────────────────────────────────────────────────────────────
    def _paste_url(self):
        try:
            text = self.clipboard_get()
            self.url_var.set(text.strip())
        except Exception:
            pass

    def _choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.output_dir)
        if d:
            self.output_dir = d
            self.dir_label.config(text=d)

    def _start_download(self):
        if self.is_downloading:
            return

        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL vazia", "Cole a URL do vídeo antes de baixar.")
            return

        if "youtube.com" not in url and "youtu.be" not in url:
            messagebox.showwarning("URL inválida", "Cole uma URL válida do YouTube.")
            return

        self.is_downloading = True
        self.btn_download.config(state="disabled", text="Buscando informações...")
        self.progress.config(mode="indeterminate")
        self.progress.start(12)
        self._set_status("Buscando informações do vídeo...", TEXT_DIM)

        threading.Thread(target=self._fetch_info, args=(url,), daemon=True).start()

    def _fetch_info(self, url):
        try:
            opts = {"quiet": True, "no_warnings": True, "noplaylist": True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False)
            if info is None:
                self.after(0, self._on_error, "Vídeo indisponível ou URL inválida.")
                return
            self.after(0, self._show_confirm_dialog, info)
        except Exception as e:
            self.after(0, self._on_error, str(e))

    # ── Diálogo de confirmação ────────────────────────────────────────────────
    def _show_confirm_dialog(self, info):
        self.progress.stop()
        self._done()
        self._set_status("Aguardando confirmação...", TEXT_DIM)

        entries = [e for e in (info.get("entries") or [info]) if e is not None]

        dialog = tk.Toplevel(self)
        dialog.title("Confirmar Download")
        dialog.configure(bg=BG)
        dialog.resizable(False, True)
        dialog.transient(self)
        dialog.grab_set()

        # Cabeçalho
        tk.Label(dialog, text=info.get("title", "Vídeo"),
                 font=("Courier New", 12, "bold"), fg=TEXT, bg=BG,
                 wraplength=580, justify="left").pack(padx=20, pady=(16, 2), anchor="w")
        tk.Label(dialog, text=f"{len(entries)} faixa(s) encontrada(s)",
                 font=("Courier New", 9), fg=TEXT_DIM, bg=BG).pack(padx=20, anchor="w")

        tk.Frame(dialog, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(8, 0))

        # Botões empacotados primeiro (side="bottom") para garantir espaço
        tk.Frame(dialog, bg=BORDER, height=1).pack(side="bottom", fill="x", padx=20)
        btn_frame = tk.Frame(dialog, bg=BG, pady=12)
        btn_frame.pack(side="bottom", fill="x", padx=20)

        container = tk.Frame(dialog, bg=BG)
        container.pack(fill="both", expand=True, padx=20, pady=8)

        canvas = tk.Canvas(container, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)

        inner.bind("<Configure>", lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind("<Button-4>", lambda _: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda _: canvas.yview_scroll(1, "units"))

        check_vars = []
        for i, entry in enumerate(entries):
            title = entry.get("title", f"Faixa {i + 1}")
            duration = entry.get("duration") or 0
            filesize = entry.get("filesize") or entry.get("filesize_approx")

            mins, secs = divmod(int(duration), 60)
            duration_str = f"{mins}:{secs:02d}" if duration else "--:--"
            size_str = f"{filesize / 1_048_576:.1f} MB" if filesize else "?"

            row = tk.Frame(inner, bg=SURFACE, pady=6, padx=10)
            row.pack(fill="x", pady=2, padx=2)

            var = tk.BooleanVar(value=True)
            check_vars.append(var)

            tk.Checkbutton(row, variable=var, bg=SURFACE,
                           activebackground=SURFACE, selectcolor=ACCENT,
                           fg=TEXT, activeforeground=TEXT,
                           cursor="hand2").pack(side="left")

            meta = tk.Frame(row, bg=SURFACE)
            meta.pack(side="left", fill="x", expand=True, padx=(8, 0))

            tk.Label(meta, text=title, font=("Courier New", 9, "bold"),
                     fg=TEXT, bg=SURFACE, anchor="w").pack(anchor="w")
            tk.Label(meta, text=f"Duração: {duration_str}  •  Tamanho: {size_str}",
                     font=("Courier New", 8), fg=TEXT_DIM, bg=SURFACE).pack(anchor="w")

        def on_cancel():
            self._set_status("Cancelado.", TEXT_DIM)
            dialog.destroy()

        def on_start():
            selected = [e for e, v in zip(entries, check_vars) if v.get()]
            if not selected:
                messagebox.showwarning("Nenhuma selecionada",
                                       "Selecione ao menos uma faixa.", parent=dialog)
                return
            dialog.destroy()
            self.is_downloading = True
            self.btn_download.config(state="disabled", text="Baixando...")
            self.progress.config(mode="determinate", maximum=100, value=0)
            self._track_info = {"index": 0, "total": len(selected)}
            self._set_status("Iniciando download...", TEXT_DIM)
            threading.Thread(target=self._download_entries, args=(selected,), daemon=True).start()

        tk.Button(btn_frame, text="Cancelar",
                  font=("Courier New", 10), fg=TEXT, bg=BORDER,
                  relief="flat", bd=0, cursor="hand2", padx=16,
                  activeforeground=ACCENT, activebackground=BORDER,
                  command=on_cancel).pack(side="left", ipady=6)

        tk.Button(btn_frame, text="⬇  BAIXAR SELECIONADAS",
                  font=("Courier New", 10, "bold"), fg=BG, bg=ACCENT,
                  relief="flat", bd=0, cursor="hand2", padx=16,
                  activeforeground=BG, activebackground=ACCENT2,
                  command=on_start).pack(side="right", ipady=8)

        # Centraliza o diálogo na tela após calcular tamanho real
        dialog.update_idletasks()
        w, h = 640, max(dialog.winfo_reqheight(), 360)
        x = (dialog.winfo_screenwidth() - w) // 2
        y = (dialog.winfo_screenheight() - h) // 2
        dialog.geometry(f"{w}x{h}+{x}+{y}")

    # ── Download ──────────────────────────────────────────────────────────────
    def _download_entries(self, entries):
        fmt = self.format_var.get()
        quality = self.quality_var.get()
        total = len(entries)
        error_count = 0

        for i, entry in enumerate(entries):
            self._track_info["index"] = i
            title = entry.get("title", f"Faixa {i + 1}")
            self.after(0, self._set_status, f"[{i + 1}/{total}] {title}", TEXT_DIM)
            self.after(0, lambda: self.progress.config(value=0))

            url = entry.get("webpage_url") or entry.get("url")
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": fmt,
                    "preferredquality": quality,
                }],
                "progress_hooks": [self._progress_hook],
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "logger": _SilentLogger(),
                **({"ffmpeg_location": FFMPEG_PATH} if FFMPEG_PATH else {}),
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                error_count += 1
                self.after(0, self._set_status, f"✗ Erro em '{title}': {e}", ERROR)

        self.after(0, self._on_success_batch, total, error_count)

    def _progress_hook(self, d):
        idx = self._track_info["index"] + 1
        total = self._track_info["total"]

        if d["status"] == "downloading":
            pct_str = d.get("_percent_str", "").strip()
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()

            try:
                pct = float(pct_str.replace("%", "").strip())
                self.after(0, lambda v=pct: self.progress.config(value=v))
            except (ValueError, TypeError):
                pass

            parts = [f"[{idx}/{total}]", pct_str, speed]
            if eta:
                parts.append(f"ETA {eta}")
            self.after(0, self._set_status, "  ".join(p for p in parts if p), TEXT_DIM)

        elif d["status"] == "finished":
            self.after(0, lambda: self.progress.config(value=100))
            self.after(0, self._set_status,
                       f"[{idx}/{total}] Convertendo para áudio...", TEXT_DIM)

    def _on_success_batch(self, total, error_count):
        self._done()
        if error_count == 0:
            self._set_status(f"✓ {total} faixa(s) salva(s) em {self.output_dir}", SUCCESS)
            messagebox.showinfo("Download concluído",
                                f"{total} arquivo(s) salvo(s) em:\n{self.output_dir}")
        else:
            ok = total - error_count
            self._set_status(f"✓ {ok}/{total} faixa(s) salvas. {error_count} erro(s).", SUCCESS)
            messagebox.showwarning("Download com erros",
                                   f"{ok} de {total} arquivo(s) baixado(s) com sucesso.")

    def _on_error(self, err):
        self._done()
        err = re.sub(r"\x1b\[[^m]*m", "", str(err)).strip()
        if "ffmpeg" in err.lower():
            msg = "FFmpeg não encontrado. Instale com: pip install -r requirements.txt"
        elif "unavailable" in err.lower() or "not available" in err.lower():
            msg = "Vídeo indisponível ou URL inválida."
        elif "ERROR:" in err:
            msg = err.split("ERROR:")[-1].strip()
        else:
            msg = err
        self._set_status(f"✗ Erro: {msg}", ERROR)
        messagebox.showerror("Erro no download", msg)

    def _done(self):
        self.is_downloading = False
        self.progress.stop()
        self.progress.config(mode="indeterminate")
        self.btn_download.config(state="normal", text="⬇  BAIXAR ÁUDIO")

    def _set_status(self, msg, color=TEXT_DIM):
        self.status_var.set(msg)
        self.status_label.config(fg=color)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
