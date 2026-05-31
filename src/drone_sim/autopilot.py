"""
Módulo de autopiloto.

Define a classe Autopilot que gerencia a navegação automática do drone
através de diferentes estados de voo.
"""

from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .drone import Drone
    from .world import Obstacle


class Autopilot:
    """
    Gerencia a navegação automática do drone.
    
    Implementa máquina de estados para controlar o drone através de
    diferentes fases da missão: decolagem, navegação, flip, retorno e pouso.
    """

    def __init__(self) -> None:
        """
        Inicializa o autopiloto.
        
        Define os valores padrão para temporizadores e estado.
        
        Returns:
            None
        """
        self._state: str = "TAKEOFF"
        self._flip_timer: float = 0.0

    # -------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------

    @property
    def state(self) -> str:
        """
        Obtém o estado atual do autopiloto.
        
        Returns:
            String representando o estado da missão
        """
        return self._state

    # -------------------------------------------------------
    # SETTERS
    # -------------------------------------------------------

    @state.setter
    def state(self, new_state: str) -> None:
        """
        Define um novo estado para o autopiloto.
        
        Args:
            new_state: String representando o novo estado
        
        Returns:
            None
        """
        self._state = str(new_state)

    # -------------------------------------------------------
    # MÉTODOS DE CONTROLE
    # -------------------------------------------------------

    def update(self, drone: "Drone", obstacles: list, wall_y: float, 
               dt: float) -> None:
        """
        Atualiza o controle do drone baseado no estado atual.
        
        Args:
            drone: Instância do Drone a ser controlado
            obstacles: Lista de obstáculos no ambiente
            wall_y: Posição Y da parede final
            dt: Delta de tempo em segundos
        
        Returns:
            None
        """
        pos: np.ndarray = drone.position

        # TAKEOFF (Decolagem)
        if self._state == "TAKEOFF":
            self._handle_takeoff(drone)

        # NAVEGAÇÃO EM SLALOM
        elif self._state == "NAVIGATE":
            self._handle_navigate(drone, obstacles, wall_y)

        # FLIP (Rotação)
        elif self._state == "FLIP":
            self._handle_flip(drone, dt)

        # RETURN TO LAUNCH (Retorno)
        elif self._state == "RTL":
            self._handle_rtl(drone)

        # LAND (Pouso)
        elif self._state == "LAND":
            self._handle_land(drone)

    # -------------------------------------------------------
    # HANDLERS DE ESTADO
    # -------------------------------------------------------

    def _handle_takeoff(self, drone: "Drone") -> None:
        """
        Gerencia a fase de decolagem.
        
        Args:
            drone: Instância do Drone
        
        Returns:
            None
        """
        drone.apply_control(throttle=0.7, roll=0, pitch=0, yaw=0)

        if drone.position[2] >= 1.9:
            self._state = "NAVIGATE"

    def _handle_navigate(self, drone: "Drone", obstacles: list, 
                        wall_y: float) -> None:
        """
        Gerencia a fase de navegação com esquiva de obstáculos em Slalom.
        
        Args:
            drone: Instância do Drone
            obstacles: Lista de obstáculos
            wall_y: Posição Y da parede final
        
        Returns:
            None
        """
        pos: np.ndarray = drone.position
        roll_cmd: float = 0.0
        pitch_cmd: float = 1.0

        # 1º OBSTÁCULO: Esquiva pela esquerda
        if pos[1] < 1.2:
            obs_atual = obstacles[0]
            dist_y: float = obs_atual.pos[1] - pos[1]

            if dist_y < 4.5:
                target_x: float = obs_atual.pos[0] - 1.8
                roll_cmd = (target_x - pos[0]) * 1.2
                pitch_cmd = max(0.3, (dist_y / 4.5))

        # 2º OBSTÁCULO: Esquiva pela direita
        elif pos[1] < 5.8:
            obs_atual = obstacles[1]
            dist_y: float = obs_atual.pos[1] - pos[1]

            if dist_y < 4.5:
                target_x: float = obs_atual.pos[0] + 1.8
                roll_cmd = (target_x - pos[0]) * 1.2
                pitch_cmd = max(0.3, (dist_y / 4.5))
            else:
                target_x: float = 0.5
                roll_cmd = (target_x - pos[0]) * 0.8

        # PÓS-OBSTÁCULOS: Centralizar para o fim da pista
        else:
            target_x: float = 0.0
            roll_cmd = (target_x - pos[0]) * 0.8

        # Limitadores de segurança
        roll_cmd = np.clip(roll_cmd, -1.0, 1.0)
        pitch_cmd = np.clip(pitch_cmd, 0.2, 1.0)

        drone.apply_control(
            throttle=0.55, roll=roll_cmd, pitch=pitch_cmd, yaw=0
        )

        if pos[1] >= wall_y - 1:
            self._state = "FLIP"

    def _handle_flip(self, drone: "Drone", dt: float) -> None:
        """
        Gerencia a fase de rotação (flip).
        
        Args:
            drone: Instância do Drone
            dt: Delta de tempo em segundos
        
        Returns:
            None
        """
        self._flip_timer += dt

        drone.apply_control(throttle=0.65, roll=0, pitch=0, yaw=3)

        if self._flip_timer >= 1.0:
            self._flip_timer = 0.0
            self._state = "RTL"

    def _handle_rtl(self, drone: "Drone") -> None:
        """
        Gerencia a fase de retorno ao ponto de lançamento (RTL).
        
        Args:
            drone: Instância do Drone
        
        Returns:
            None
        """
        pos: np.ndarray = drone.position
        delta: np.ndarray = drone.launch_position - pos

        roll_cmd: float = np.clip(delta[0], -1, 1)
        pitch_cmd: float = np.clip(delta[1], -1, 1)

        drone.apply_control(
            throttle=0.55, roll=roll_cmd, pitch=pitch_cmd, yaw=0
        )

        if np.linalg.norm(delta[:2]) < 0.3:
            self._state = "LAND"

    def _handle_land(self, drone: "Drone") -> None:
        """
        Gerencia a fase de pouso.
        
        Args:
            drone: Instância do Drone
        
        Returns:
            None
        """
        drone.target_altitude = 0.2

        drone.apply_control(throttle=0.45, roll=0, pitch=0, yaw=0)

        if drone.position[2] <= 0.25:
            self._state = "DONE"
