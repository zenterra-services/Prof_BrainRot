# Docker Installation Guide for Windows

Docker is the easiest way to run your ProfBrainRot system. Here are the installation options:

## 🚀 Quick Install Options

### Option A: Docker Desktop (Recommended)
1. **Download Docker Desktop**: https://docker.com/products/docker-desktop
2. **Install**: Run the installer and follow prompts
3. **Restart**: Restart your computer when prompted
4. **Verify**: Open PowerShell and run: `docker --version`

### Option B: Docker via Chocolatey (Advanced)
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Docker
choco install docker-desktop -y
```

## 🔧 Alternative: Manual Setup Without Docker

If you prefer not to install Docker, see `MANUAL_SETUP.md` for standalone installation.

## ✅ After Installation

Once Docker is installed, return to the main setup:
```bash
cd n8n
docker-compose up -d
```

## 🆘 Troubleshooting

If Docker installation fails:
1. Check Windows version (Windows 10 Pro/Enterprise recommended)
2. Enable virtualization in BIOS
3. Try Docker Toolbox for older Windows versions
4. Use the manual setup option instead