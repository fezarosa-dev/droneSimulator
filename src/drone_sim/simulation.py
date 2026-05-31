"""
Módulo de simulação.

Define a classe Simulation que gerencia o loop principal da simulação
do drone, física e detecção de colisões.
"""

from typing import List
import vpython as vp
import numpy as np
from drone_sim.drone import Drone
from drone_sim.world import WorldGenerator, Obstacle
from drone_sim.autopilot import Autopilot


class Simulation:
    """
    Gerencia o loop principal da simulação do drone.
    
    Responsável por coordenar o mundo, o drone, a física e o autopiloto.
    """

    def __init__(self) -> None:
        """
        Inicializa a simulação criando o mundo e o drone.
        
        Cria o gerador de mundo e gera o ambiente completo, depois
        cria o drone e inicializa as variáveis de estado.
        
        Returns:
            None
        """
        # Geração do mundo
        self._world_generator: WorldGenerator = WorldGenerator()
        self._world_generator.generate()

        self._obstacles: List[Obstacle] = self._world_generator.get_obstacles()
        self._wall_y: float = self._world_generator.get_wall_y()

        self._drone: Drone = Drone()
        self._autopilot: Autopilot = Autopilot()
        self._dt: float = 0.02
        self._time: float = 0.0
        self._last_log: int = -1

    # -------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------

    @property
    def state(self) -> str:
        """
        Obtém o estado atual da simulação (do autopiloto).
        
        Returns:
            String representando o estado da missão
        """
        return self._autopilot.state

    @property
    def time(self) -> float:
        """
        Obtém o tempo decorrido na simulação.
        
        Returns:
            Valor float do tempo em segundos
        """
        return self._time

    @property
    def drone(self) -> Drone:
        """
        Obtém a instância do drone.
        
        Returns:
            Objeto Drone da simulação
        """
        return self._drone

    @property
    def autopilot(self) -> Autopilot:
        """
        Obtém a instância do autopiloto.
        
        Returns:
            Objeto Autopilot da simulação
        """
        return self._autopilot

    @property
    def obstacles(self) -> List[Obstacle]:
        """
        Obtém a lista de obstáculos.
        
        Returns:
            Lista contendo todos os Obstacle da simulação
        """
        return self._obstacles.copy()

    @property
    def wall_y(self) -> float:
        """
        Obtém a posição Y da parede final.
        
        Returns:
            Valor float da coordenada Y em metros
        """
        return self._wall_y

    # -------------------------------------------------------
    # SENSOR LOG
    # -------------------------------------------------------

    def log_sensors(self) -> None:
        """
        Registra os dados dos sensores a cada segundo.
        
        Imprime GPS, LIDAR e IMU com as informações de estado e tempo.
        
        Returns:
            None
        """
        second: int = int(self._time)
        if second == self._last_log:
            return
        self._last_log = second

        gps: np.ndarray = self._drone.gps()
        imu: dict = self._drone.imu()
        lidar: float = self._drone.lidar()

        print(
            f"[{self._time:.1f}s] "
            f"{self._autopilot.state:10} | "
            f"GPS=({gps[0]:.2f}, {gps[1]:.2f}, {gps[2]:.2f}) | "
            f"LiDAR={lidar:.2f}m | "
            f"Roll={imu['roll']:.2f} | "
            f"Pitch={imu['pitch']:.2f} | "
            f"Yaw={imu['yaw']:.2f}"
        )

    # -------------------------------------------------------
    # DETECÇÃO DE COLISÃO
    # -------------------------------------------------------

    def _check_collisions(self) -> bool:
        """
        Verifica se o drone colidiu com algum obstáculo.
        
        Returns:
            True se houve colisão, False caso contrário
        """
        for obs in self._obstacles:
            if obs.collides(self._drone.position, self._drone.radius):
                return True
        return False

    # -------------------------------------------------------
    # LOOP PRINCIPAL
    # -------------------------------------------------------

    def run(self) -> None:
        """
        Executa o loop principal da simulação.
        
        Executa iterativamente o autopiloto, atualiza a física do drone,
        verifica colisões e registra sensores até a missão estar concluída.
        
        Returns:
            None
        """
        print("INICIANDO MISSÃO...\n")

        while self._autopilot.state != "DONE":
            vp.rate(60)

            # Atualiza autopiloto
            self._autopilot.update(
                self._drone, 
                self._obstacles, 
                self._wall_y, 
                self._dt
            )

            # Atualiza física do drone
            self._drone.update(self._dt)

            # Verifica colisão
            if self._check_collisions():
                print("\nCOLISÃO!")
                self._drone.crashed = True
                return

            self.log_sensors()
            self._time += self._dt

        print("\nMISSÃO CONCLUÍDA!")


