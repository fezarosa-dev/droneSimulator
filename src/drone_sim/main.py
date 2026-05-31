"""
Módulo principal do simulador de drone.

Inicializa e executa a simulação com controle do autopiloto.
"""

from drone_sim.simulation import Simulation


def main() -> None:
    """
    Função principal que executa a simulação do drone.
    
    Cria uma instância da simulação e executa o loop principal.
    
    Returns:
        None
    """
    sim: Simulation = Simulation()
    sim.run()


if __name__ == "__main__":
    main()

