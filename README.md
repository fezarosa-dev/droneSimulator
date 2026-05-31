# Drone Simulator

Projeto de simulação de drone usando **VPython** e **NumPy**, desenvolvido no ambiente do **ROS 2**.

---

## Requisitos

- Python 3.10+
- pip

---

## Instalação

Clone o repositório:

```bash
git clone https://github.com/fezarosa-dev/droneSimulator
cd droneSimulator
```

Execute o script de setup:

```bash
chmod +x script/setup.sh
./script/setup.sh
```

---

## Atualização do projeto

Sempre que `pyproject.toml` ou `requirements.txt` forem alterados:

```bash
chmod +x script/update.sh
./script/update.sh
```

---

## Como rodar o simulador

Após instalação, você pode executar de qualquer lugar:

```bash
drone-sim
```

Ou diretamente pelo módulo:

```bash
python3 -m drone_sim.main
```

---

## Estrutura do projeto

```
droneSimulator/
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

O comando `drone-sim` é definido via `pyproject.toml`:

```toml
[project.scripts]
drone-sim = "drone_sim.main:run"
```

---

## Problemas comuns

### Comando não encontrado (drone-sim)

Se o comando não for encontrado após o setup:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Para solução permanente, adicione ao `.bashrc` ou `.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```