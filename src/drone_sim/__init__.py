"""
Simulador de Drone - Um simulador de voo para quadricópteros usando VPython.

Pacotes:
- drone: Gerencia o quadricóptero e sua dinâmica
- world: Gerencia a criação e configuração do ambiente de simulação
- autopilot: Gerencia a navegação automática do drone
- simulation: Controla o loop principal da simulação
"""

from .drone import Drone
from .world import Obstacle, WorldGenerator
from .autopilot import Autopilot
from .simulation import Simulation

__all__ = ["Drone", "Obstacle", "WorldGenerator", "Autopilot", "Simulation"]

