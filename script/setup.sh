#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Entrando no projeto: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "Atualizando pip para o usuário..."
python3 -m pip install --upgrade pip --user

echo "Instalando dependências globais..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --user
else
    echo "Aviso: requirements.txt não encontrado, pulando..."
fi

echo "Instalando projeto em modo editável..."
python3 -m pip install -e . --user

echo ""
echo "Setup concluído com sucesso."
echo ""
echo "Para rodar o simulador use:"
echo "  drone-sim"
echo "ou:"
echo "  python3 -m drone_sim.main"
echo ""