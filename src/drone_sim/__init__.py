"""
Simulador de Drone - Um simulador de voo para quadricópteros usando VPython.

Pacotes:
- drone: Gerencia o quadricóptero e sua dinâmica
- world: Gerencia a criação e configuração do ambiente de simulação
- simulation: Controla a simulação completa
"""

from .drone import Drone
from .world import Obstacle, WorldGenerator
from .simulation import Simulation

__all__ = ["Drone", "Obstacle", "WorldGenerator", "Simulation"]
