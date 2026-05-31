#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Entrando no projeto: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Criar venv apenas se não existir
if [ ! -d "venv" ]; then
    echo "Criando venv..."
    python3 -m venv venv
else
    echo "venv já existe, pulando criação..."
fi

echo "Ativando venv..."
source venv/bin/activate

echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Instalando projeto em modo editável..."
pip install -e .

echo "Gerando freeze do ambiente..."
pip freeze > requirements.lock.txt

echo ""
echo "Setup concluído com sucesso."
echo ""
echo "Para rodar o simulador use:"
echo "  drone-sim"
echo "ou:"
echo "  python -m drone_sim.main"
echo ""
echo "Para reativar o ambiente depois:"
echo "  source venv/bin/activate"