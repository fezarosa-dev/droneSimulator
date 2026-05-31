#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Entrando no projeto: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

echo "Ativando venv..."
source venv/bin/activate

echo "Atualizando pip..."
pip install --upgrade pip

echo "Atualizando dependências do requirements.txt..."
pip install -r requirements.txt

echo "Reinstalando projeto em modo editável..."
pip install -e .

echo "Gerando lock atualizado..."
pip freeze > requirements.lock.txt

echo ""
echo "Update concluído com sucesso."
echo "Agora você pode rodar: drone-sim"