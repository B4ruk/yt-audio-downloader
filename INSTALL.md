# Instalação — YT Audio Downloader

Nenhuma versão precisa de Python ou FFmpeg instalados: tudo já vem dentro do pacote.

| Sistema | Arquivo |
|---|---|
| Windows (recomendado) | `YT-Audio-Downloader-<versão>-windows-x64-setup.exe` |
| Windows (portátil) | `YT-Audio-Downloader-<versão>-windows-x64-portable.zip` |
| Linux | `YT-Audio-Downloader-<versão>-linux-x86_64.zip` |
| macOS (Apple Silicon) | `YT-Audio-Downloader-<versão>-macos-arm64.zip` |

---

## Windows

### Instalador (.exe)

1. Baixe o arquivo `…-windows-x64-setup.exe`.
2. Dê dois cliques nele.
3. Se o Windows exibir **"O Windows protegeu o computador"**, clique em **Mais informações → Executar assim mesmo**. O aviso aparece porque o instalador não tem assinatura digital paga.
4. Siga o assistente: aceite a licença, escolha a pasta e marque se quer um atalho na Área de Trabalho.
5. Abra o programa pelo **Menu Iniciar → YT Audio Downloader**.

Para desinstalar, use **Configurações → Aplicativos → YT Audio Downloader → Desinstalar**.

### Portátil (.zip)

1. Baixe o `…-windows-x64-portable.zip`.
2. Clique com o botão direito → **Extrair tudo…**
3. Abra a pasta extraída e execute `YT-Audio-Downloader.exe`.

Não instala nada no sistema. Para remover, apague a pasta.

---

## Linux

Testado em Ubuntu 22.04+, Debian 12+, Fedora 38+ e Linux Mint 21+ (x86_64).

### Instalar

```bash
cd ~/Downloads
unzip YT-Audio-Downloader-*-linux-x86_64.zip
cd YT-Audio-Downloader-*-linux-x86_64
./install.sh
```

O script copia o programa para `~/.local/bin` e cria o atalho no menu de aplicativos, sem precisar de `sudo`. Depois disso, procure **YT Audio Downloader** no menu ou rode `yt-audio-downloader` no terminal.

Se aparecer `Permissão negada`:

```bash
chmod +x install.sh uninstall.sh YT-Audio-Downloader
./install.sh
```

### Usar sem instalar

```bash
./YT-Audio-Downloader
```

### Desinstalar

```bash
./uninstall.sh
```

---

## macOS

Requer macOS 12 ou superior em Mac com chip Apple (M1/M2/M3/M4).

### Instalar

1. Baixe o `…-macos-arm64.zip` e dê dois cliques para extrair.
2. Arraste **YT-Audio-Downloader.app** para a pasta **Aplicativos**.
3. Na **primeira vez**, clique com o botão direito no app → **Abrir** → **Abrir**. O app não é assinado pela Apple, então o duplo clique normal é bloqueado.

Se o macOS disser que o app **"está danificado"**, rode no Terminal:

```bash
xattr -dr com.apple.quarantine /Applications/YT-Audio-Downloader.app
```

### Desinstalar

Arraste **YT-Audio-Downloader.app** da pasta Aplicativos para o Lixo.

---

## Verificando o download (opcional)

Cada release traz o arquivo `SHA256SUMS.txt`. Para conferir se o arquivo baixado está íntegro:

```bash
sha256sum -c SHA256SUMS.txt --ignore-missing       # Linux
shasum -a 256 -c SHA256SUMS.txt --ignore-missing   # macOS
```

```powershell
Get-FileHash .\YT-Audio-Downloader-*-setup.exe     # Windows (PowerShell)
```
