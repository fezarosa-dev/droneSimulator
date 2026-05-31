"""
Módulo principal do simulador de drone.
Inicializa e executa a simulação.
"""

from .simulation import Simulation


def run():
    """Executa a simulação do drone."""
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    run()
