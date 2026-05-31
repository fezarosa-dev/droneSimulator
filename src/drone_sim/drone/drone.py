import vpython as vp
import numpy as np


class Drone:
    """
    Representa um drone quadricóptero na simulação.
    """

    def __init__(self):
        """Inicializa o drone com posição, orientação e sensores padrões."""
        self.launch_position = np.array([0.0, -4.0, 0.3])
        self.position = self.launch_position.copy()
        self.velocity = np.zeros(3)
        self.radius = 0.15

        # orientação
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0

        self.target_altitude = 2.0

        # motores
        self.motor_power = np.zeros(4)
        self.crashed = False

        self.create_visual()

    # -------------------------------------------------------
    # VISUAL
    # -------------------------------------------------------

    def create_visual(self):
        """Cria a representação visual do drone no VPython."""
        self.center = vp.sphere(
            pos=vp.vector(*self.position),
            radius=0.12,
            color=vp.color.blue,
            make_trail=True,
            retain=500,
        )

        self.arm_offsets = [
            np.array([0.35, 0.35, 0]),
            np.array([-0.35, 0.35, 0]),
            np.array([0.35, -0.35, 0]),
            np.array([-0.35, -0.35, 0]),
        ]

        self.arms = []

        for offset in self.arm_offsets:
            arm = vp.cylinder(
                pos=self.center.pos,
                axis=vp.vector(*offset),
                radius=0.02,
                color=vp.color.black,
            )
            self.arms.append(arm)

        motor_colors = [vp.color.red, vp.color.green, vp.color.orange, vp.color.purple]

        self.motors_visual = []

        for i, offset in enumerate(self.arm_offsets):
            # Posiciona o motor ligeiramente acima do braço (Z + 0.04)
            motor_pos = self.center.pos + vp.vector(
                offset[0], offset[1], offset[2] + 0.04
            )

            motor = vp.sphere(pos=motor_pos, radius=0.06, color=motor_colors[i])

            self.motors_visual.append(motor)

    # -------------------------------------------------------
    # CONTROLE
    # -------------------------------------------------------

    def apply_control(self, throttle, roll, pitch, yaw):
        """
        Aplica comandos de controle ao drone.
        
        Args:
            throttle: Comando de aceleração (0 a 1)
            roll: Comando de inclinação lateral (-1 a 1)
            pitch: Comando de inclinação frontal (-1 a 1)
            yaw: Comando de rotação (-1 a 1)
        """
        # motor mixing quad X
        self.motor_power[0] = throttle + roll + pitch + yaw
        self.motor_power[1] = throttle - roll + pitch - yaw
        self.motor_power[2] = throttle + roll - pitch - yaw
        self.motor_power[3] = throttle - roll - pitch + yaw

        self.motor_power = np.clip(self.motor_power, 0, 1)

        self.roll = roll
        self.pitch = pitch
        self.yaw += yaw * 0.03

    # -------------------------------------------------------
    # FÍSICA
    # -------------------------------------------------------

    def update(self, dt):
        """
        Atualiza a posição e velocidade do drone.
        
        Args:
            dt: Delta de tempo (segundos)
        """
        if self.crashed:
            return

        # roll move x
        self.velocity[0] = self.roll * 1.5

        # pitch move y
        self.velocity[1] = self.pitch * 1.5

        # throttle from average motor power
        throttle = np.mean(self.motor_power)
        climb_speed = (throttle - 0.5) * 4
        altitude_error = self.target_altitude - self.position[2]

        self.velocity[2] = climb_speed + altitude_error * 1.5

        self.position += self.velocity * dt

        # chão
        if self.position[2] < self.radius:
            self.position[2] = self.radius

        self.update_visual(dt)

    # -------------------------------------------------------
    # VISUAL UPDATE
    # -------------------------------------------------------

    def update_visual(self, dt):
        """Atualiza a visualização do drone."""
        center_pos = vp.vector(*self.position)
        self.center.pos = center_pos

        for i in range(4):
            offset = self.arm_offsets[i]

            # Atualiza posição do motor acompanhando o centro + elevação em Z
            motor_pos = center_pos + vp.vector(offset[0], offset[1], offset[2] + 0.04)

            self.motors_visual[i].pos = motor_pos
            self.arms[i].pos = center_pos

    # -------------------------------------------------------
    # SENSORES
    # -------------------------------------------------------

    def gps(self):
        """Retorna a posição GPS do drone."""
        return self.position.copy()

    def lidar(self):
        """Retorna a altitude medida pelo LIDAR."""
        return self.position[2]

    def imu(self):
        """Retorna os dados da IMU (orientação)."""
        return {"roll": self.roll, "pitch": self.pitch, "yaw": self.yaw}
