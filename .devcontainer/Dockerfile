# .devcontainer/Dockerfile

# Imagem base oficial para Dev Containers (inclui Python, Node.js, Go, etc.)
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Permite usar bash como shell padrão
SHELL ["/bin/bash", "-lc"]

# Instalações adicionais
RUN \
  set -euo pipefail && \
  apt-get update && \
  # Git e GitHub CLI
  apt-get install -y git curl gh && \
  # Limpeza
  apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria um diretório de trabalho e garante permissões
WORKDIR /workspace

# Garante que o usuário codespace tenha permissão total
RUN chown -R vscode:vscode /workspace
