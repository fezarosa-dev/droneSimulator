#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Entrando no projeto: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "Criando venv..."
python3 -m venv venv

echo "Ativando venv..."
source venv/bin/activate

echo "Atualizando pip..."
pip install --upgrade pip

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Gerando freeze do ambiente..."
pip freeze > requirements.lock.txt

echo "Setup concluído."
echo "Ative com: source venv/bin/activate"