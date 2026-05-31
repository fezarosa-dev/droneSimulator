"""
Módulo do drone.

Define a classe Drone que representa um quadricóptero com física,
visualização e sensores.
"""

from typing import Tuple, Dict
import vpython as vp
import numpy as np


class Drone:
    """
    Representa um quadricóptero na simulação.
    
    O drone possui modelo de dinâmica de voo simplificado, quatro motores,
    sensores (GPS, LIDAR, IMU) e visualização em VPython.
    """

    def __init__(self) -> None:
        """
        Inicializa o drone com estado padrão.
        
        Define posição de lançamento, velocidade zero, orientação neutra,
        motores desligados e cria a visualização.
        
        Returns:
            None
        """
        self._launch_position: np.ndarray = np.array([0.0, -4.0, 0.3])
        self._position: np.ndarray = self._launch_position.copy()
        self._velocity: np.ndarray = np.zeros(3)
        self._radius: float = 0.15

        # Orientação (ângulos de Euler)
        self._roll: float = 0.0
        self._pitch: float = 0.0
        self._yaw: float = 0.0

        self._target_altitude: float = 2.0

        # Motores (valores 0 a 1)
        self._motor_power: np.ndarray = np.zeros(4)
        self._crashed: bool = False

        # Dados visuais
        self._center: vp.sphere = None
        self._arms: list = []
        self._arm_offsets: list = []
        self._motors_visual: list = []

        self._create_visual()

    # -------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------

    @property
    def launch_position(self) -> np.ndarray:
        """
        Obtém a posição de lançamento do drone.
        
        Returns:
            Array numpy com coordenadas [x, y, z] da posição de lançamento
        """
        return self._launch_position.copy()

    @property
    def position(self) -> np.ndarray:
        """
        Obtém a posição atual do drone.
        
        Returns:
            Array numpy com coordenadas [x, y, z] da posição atual
        """
        return self._position.copy()

    @property
    def velocity(self) -> np.ndarray:
        """
        Obtém a velocidade atual do drone.
        
        Returns:
            Array numpy com velocidades [vx, vy, vz]
        """
        return self._velocity.copy()

    @property
    def radius(self) -> float:
        """
        Obtém o raio de colisão do drone.
        
        Returns:
            Valor float do raio em metros
        """
        return self._radius

    @property
    def roll(self) -> float:
        """
        Obtém o ângulo de roll (inclinação lateral).
        
        Returns:
            Valor float em radianos
        """
        return self._roll

    @property
    def pitch(self) -> float:
        """
        Obtém o ângulo de pitch (inclinação frontal).
        
        Returns:
            Valor float em radianos
        """
        return self._pitch

    @property
    def yaw(self) -> float:
        """
        Obtém o ângulo de yaw (rotação).
        
        Returns:
            Valor float em radianos
        """
        return self._yaw

    @property
    def target_altitude(self) -> float:
        """
        Obtém a altitude alvo do drone.
        
        Returns:
            Valor float em metros
        """
        return self._target_altitude

    @property
    def motor_power(self) -> np.ndarray:
        """
        Obtém a potência atual dos motores.
        
        Returns:
            Array numpy com potências [m0, m1, m2, m3] (0 a 1)
        """
        return self._motor_power.copy()

    @property
    def crashed(self) -> bool:
        """
        Verifica se o drone colidiu.
        
        Returns:
            True se colidiu, False caso contrário
        """
        return self._crashed

    # -------------------------------------------------------
    # SETTERS
    # -------------------------------------------------------

    @position.setter
    def position(self, new_position: np.ndarray) -> None:
        """
        Define uma nova posição para o drone.
        
        Args:
            new_position: Array com coordenadas [x, y, z]
        
        Returns:
            None
        """
        self._position = np.array(new_position, dtype=float)

    @target_altitude.setter
    def target_altitude(self, altitude: float) -> None:
        """
        Define a altitude alvo do drone.
        
        Args:
            altitude: Altitude alvo em metros
        
        Returns:
            None
        """
        self._target_altitude = float(altitude)

    @crashed.setter
    def crashed(self, value: bool) -> None:
        """
        Define o estado de colisão do drone.
        
        Args:
            value: True se colidiu, False caso contrário
        
        Returns:
            None
        """
        self._crashed = bool(value)

    # -------------------------------------------------------
    # VISUAL
    # -------------------------------------------------------

    def _create_visual(self) -> None:
        """
        Cria a representação visual do drone no VPython.
        
        Cria esfera central, braços (cilindros) e motores (esferas).
        
        Returns:
            None
        """
        self._center = vp.sphere(
            pos=vp.vector(*self._position),
            radius=0.12,
            color=vp.color.blue,
            make_trail=True,
            retain=500,
        )

        self._arm_offsets = [
            np.array([0.35, 0.35, 0]),
            np.array([-0.35, 0.35, 0]),
            np.array([0.35, -0.35, 0]),
            np.array([-0.35, -0.35, 0]),
        ]

        self._arms = []

        for offset in self._arm_offsets:
            arm = vp.cylinder(
                pos=self._center.pos,
                axis=vp.vector(*offset),
                radius=0.02,
                color=vp.color.black,
            )
            self._arms.append(arm)

        motor_colors = [vp.color.red, vp.color.green, vp.color.orange, vp.color.purple]

        self._motors_visual = []

        for i, offset in enumerate(self._arm_offsets):
            motor_pos = self._center.pos + vp.vector(
                offset[0], offset[1], offset[2] + 0.04
            )

            motor = vp.sphere(pos=motor_pos, radius=0.06, color=motor_colors[i])
            self._motors_visual.append(motor)

    # -------------------------------------------------------
    # CONTROLE
    # -------------------------------------------------------

    def apply_control(self, throttle: float, roll: float, 
                     pitch: float, yaw: float) -> None:
        """
        Aplica comandos de controle ao drone.
        
        Realiza o "motor mixing" para quadricóptero em configuração X
        e atualiza os ângulos de atitude.
        
        Args:
            throttle: Comando de aceleração (0 a 1)
            roll: Comando de inclinação lateral (-1 a 1)
            pitch: Comando de inclinação frontal (-1 a 1)
            yaw: Comando de rotação (-1 a 1)
        
        Returns:
            None
        """
        # Motor mixing para quadricóptero X
        self._motor_power[0] = throttle + roll + pitch + yaw
        self._motor_power[1] = throttle - roll + pitch - yaw
        self._motor_power[2] = throttle + roll - pitch - yaw
        self._motor_power[3] = throttle - roll - pitch + yaw

        self._motor_power = np.clip(self._motor_power, 0, 1)

        self._roll = float(roll)
        self._pitch = float(pitch)
        self._yaw += yaw * 0.03

    # -------------------------------------------------------
    # FÍSICA
    # -------------------------------------------------------

    def update(self, dt: float) -> None:
        """
        Atualiza a posição e velocidade do drone.
        
        Integra as equações de movimento simplificadas e garante que
        o drone não penetra o solo.
        
        Args:
            dt: Delta de tempo em segundos
        
        Returns:
            None
        """
        if self._crashed:
            return

        # Roll produz movimento em X
        self._velocity[0] = self._roll * 1.5

        # Pitch produz movimento em Y
        self._velocity[1] = self._pitch * 1.5

        # Throttle e altitude alvo controlam movimento em Z
        throttle: float = np.mean(self._motor_power)
        climb_speed: float = (throttle - 0.5) * 4
        altitude_error: float = self._target_altitude - self._position[2]

        self._velocity[2] = climb_speed + altitude_error * 1.5

        self._position += self._velocity * dt

        # Colisão com o solo
        if self._position[2] < self._radius:
            self._position[2] = self._radius

        self._update_visual(dt)

    # -------------------------------------------------------
    # VISUAL UPDATE
    # -------------------------------------------------------

    def _update_visual(self, dt: float) -> None:
        """
        Atualiza a visualização do drone em VPython.
        
        Args:
            dt: Delta de tempo em segundos (não utilizado neste método)
        
        Returns:
            None
        """
        center_pos = vp.vector(*self._position)
        self._center.pos = center_pos

        for i in range(4):
            offset = self._arm_offsets[i]

            motor_pos = center_pos + vp.vector(offset[0], offset[1], offset[2] + 0.04)

            self._motors_visual[i].pos = motor_pos
            self._arms[i].pos = center_pos

    # -------------------------------------------------------
    # SENSORES
    # -------------------------------------------------------

    def gps(self) -> np.ndarray:
        """
        Obtém leitura do sensor GPS.
        
        Returns:
            Array numpy com posição [x, y, z] em metros
        """
        return self._position.copy()

    def lidar(self) -> float:
        """
        Obtém leitura do sensor LIDAR (altitude).
        
        Returns:
            Valor float da altitude em metros
        """
        return float(self._position[2])

    def imu(self) -> Dict[str, float]:
        """
        Obtém leitura do sensor IMU (Inertial Measurement Unit).
        
        Returns:
            Dicionário com chaves 'roll', 'pitch', 'yaw' e valores em radianos
        """
        return {
            "roll": float(self._roll), 
            "pitch": float(self._pitch), 
            "yaw": float(self._yaw)
        }

