#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Entrando no projeto: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "Atualizando pip para o usuário..."
python3 -m pip install --upgrade pip --user

echo "Atualizando dependências do requirements.txt..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --user
else
    echo "Aviso: requirements.txt não encontrado, pulando..."
fi

echo "Reinstalando projeto e ferramentas de dev em modo editável..."
python3 -m pip install -e ".[dev]" --user

echo ""
echo "Update concluído com sucesso."
echo "Agora você pode rodar: drone-sim"
echo ""