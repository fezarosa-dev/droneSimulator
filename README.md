# Drone Simulator

Projeto de simulação de drone usando VPython e NumPy.

---

## Requisitos

- Python 3.10+
- pip
- venv

---

## Instalação

Clone o projeto:

```bash
git clone <repo>
cd drone_simulator
```

Crie o ambiente e instale dependências:

```bash
chmod +x script/setup.sh
./script/setup.sh
```

---

## Atualização do projeto

Sempre que alterar dependências ou o projeto:

```bash
chmod +x script/update.sh
./script/update.sh
```

---

## Como rodar o simulador

Após instalar:

```bash
source venv/bin/activate
drone-sim
```

ou

```bash
python -m drone_sim.main
```

---

## Estrutura do projeto

```
drone_simulator/
├── pyproject.toml
├── requirements.txt
├── script/
│   ├── setup.sh
│   └── update.sh
└── src/
    └── drone_sim/
        ├── __init__.py
        └── main.py
```

---

## Entry point

O projeto usa entry point definido no pyproject.toml:

```toml
[project.scripts]
drone-sim = "drone_sim.main:run"
```

---

## Problemas comuns

### comando não encontrado (drone-sim)

Execute:

```bash
pip install -e .
```

### ambiente errado

Sempre ative o venv:

```bash
source venv/bin/activate
```