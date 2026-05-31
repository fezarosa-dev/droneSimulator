import vpython as vp
import numpy as np

# ============================================================
# OBSTÁCULOS
# ============================================================


class Obstacle:

    def __init__(self, pos, size, color):

        self.pos = np.array(pos, dtype=float)
        self.size = np.array(size, dtype=float)

        self.visual = vp.box(pos=vp.vector(*pos), size=vp.vector(*size), color=color)

    def collides(self, drone_pos, radius):

        delta = np.abs(drone_pos - self.pos)

        return (
            delta[0] <= self.size[0] / 2 + radius
            and delta[1] <= self.size[1] / 2 + radius
            and delta[2] <= self.size[2] / 2 + radius
        )


# ============================================================
# DRONE
# ============================================================


class Drone:

    def __init__(self):

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
        return self.position.copy()

    def lidar(self):
        return self.position[2]

    def imu(self):
        return {"roll": self.roll, "pitch": self.pitch, "yaw": self.yaw}


# ============================================================
# SIMULAÇÃO
# ============================================================


class Simulation:

    def __init__(self):

        vp.canvas(
            title="Drone Simulator - Slalom Perfeito por Fora (Sem Hélices)",
            width=1400,
            height=900,
            background=vp.color.white,
        )

        # Reposiciona a câmera do VPython para olhar o drone de cima em diagonal
        vp.scene.camera.pos = vp.vector(0, -9, 6)
        vp.scene.camera.axis = vp.vector(0, 9, -5)

        # chão ampliado para acomodar o trajeto mais longo
        vp.box(
            pos=vp.vector(0, 2, -0.1), size=vp.vector(16, 24, 0.2), color=vp.color.green
        )

        # parede final colocada mais longe (de 5 para 10)
        self.wall_y = 10

        vp.box(
            pos=vp.vector(0, self.wall_y, 1),
            size=vp.vector(8, 0.2, 2),
            color=vp.color.red,
        )

        # Obstáculos reposicionados estrategicamente para o Slalom
        self.obstacles = [
            Obstacle(
                [-1.2, 0.0, 1],  # 1º Obstáculo (Esquerda - Laranja)
                [1, 1, 2],
                vp.color.orange,
            ),
            Obstacle(
                [1.2, 4.5, 1],  # 2º Obstáculo (Direita - Roxo)
                [1, 1, 2],
                vp.color.purple,
            ),
        ]

        self.drone = Drone()
        self.state = "TAKEOFF"
        self.dt = 0.02
        self.time = 0
        self.flip_timer = 0
        self.last_log = -1

    # -------------------------------------------------------
    # AUTOPILOTO
    # -------------------------------------------------------

    def autopilot(self):

        pos = self.drone.position

        # TAKEOFF (Decolagem)
        if self.state == "TAKEOFF":

            self.drone.apply_control(throttle=0.7, roll=0, pitch=0, yaw=0)

            if pos[2] >= 1.9:
                self.state = "NAVIGATE"

        # NAVEGAÇÃO EM SLALOM (SEMPRE POR FORA)
        elif self.state == "NAVIGATE":

            roll_cmd = 0.0
            pitch_cmd = 1.0  # Velocidade padrão para frente

            # 1º OBSTÁCULO: Foca na esquiva pela Esquerda até ultrapassá-lo em Y
            if pos[1] < 1.2:
                obs_atual = self.obstacles[0]
                dist_y = obs_atual.pos[1] - pos[1]

                # Começa a desviar com bastante antecedência (4.5m)
                if dist_y < 4.5:
                    # Rota de fuga externa bem ampla à esquerda (X mais negativo)
                    target_x = obs_atual.pos[0] - 1.8
                    roll_cmd = (target_x - pos[0]) * 1.2

                    # Reduz o passo frontal para evitar a derrapagem por inércia
                    pitch_cmd = max(0.3, (dist_y / 4.5))

            # 2º OBSTÁCULO: Ativado após passar o primeiro
            elif pos[1] < 5.8:
                obs_atual = self.obstacles[1]
                dist_y = obs_atual.pos[1] - pos[1]

                if dist_y < 4.5:
                    # Rota de fuga externa bem ampla à direita (X mais positivo)
                    target_x = obs_atual.pos[0] + 1.8
                    roll_cmd = (target_x - pos[0]) * 1.2

                    # Reduz a velocidade para frente proporcionalmente para fazer a curva limpa
                    pitch_cmd = max(0.3, (dist_y / 4.5))
                else:
                    # Transição dinâmica: cruzando em diagonal suave logo após passar o 1º bloco
                    target_x = 0.5
                    roll_cmd = (target_x - pos[0]) * 0.8

            # PÓS-OBSTÁCULOS: Centraliza o drone para o final da pista
            else:
                target_x = 0.0
                roll_cmd = (target_x - pos[0]) * 0.8

            # Limitadores de segurança física
            roll_cmd = np.clip(roll_cmd, -1.0, 1.0)
            pitch_cmd = np.clip(pitch_cmd, 0.2, 1.0)

            self.drone.apply_control(
                throttle=0.55, roll=roll_cmd, pitch=pitch_cmd, yaw=0
            )

            if pos[1] >= self.wall_y - 1:
                self.state = "FLIP"

        # FLIP
        elif self.state == "FLIP":

            self.flip_timer += self.dt

            self.drone.apply_control(throttle=0.65, roll=0, pitch=0, yaw=3)

            if self.flip_timer >= 1:
                self.flip_timer = 0
                self.state = "RTL"

        # RETURN TO LAUNCH
        elif self.state == "RTL":

            delta = self.drone.launch_position - pos

            roll_cmd = np.clip(delta[0], -1, 1)
            pitch_cmd = np.clip(delta[1], -1, 1)

            self.drone.apply_control(
                throttle=0.55, roll=roll_cmd, pitch=pitch_cmd, yaw=0
            )

            if np.linalg.norm(delta[:2]) < 0.3:
                self.state = "LAND"

        # LAND
        elif self.state == "LAND":

            self.drone.target_altitude = 0.2

            self.drone.apply_control(throttle=0.45, roll=0, pitch=0, yaw=0)

            if pos[2] <= 0.25:
                self.state = "DONE"

    # -------------------------------------------------------
    # SENSOR LOG
    # -------------------------------------------------------

    def log_sensors(self):

        second = int(self.time)
        if second == self.last_log:
            return
        self.last_log = second

        gps = self.drone.gps()
        imu = self.drone.imu()
        lidar = self.drone.lidar()

        print(
            f"[{self.time:.1f}s] "
            f"{self.state:10} | "
            f"GPS=({gps[0]:.2f}, {gps[1]:.2f}, {gps[2]:.2f}) | "
            f"LiDAR={lidar:.2f}m | "
            f"Roll={imu['roll']:.2f} | "
            f"Pitch={imu['pitch']:.2f} | "
            f"Yaw={imu['yaw']:.2f}"
        )

    # -------------------------------------------------------
    # LOOP
    # -------------------------------------------------------

    def run(self):

        print("INICIANDO MISSÃO...\n")

        while self.state != "DONE":

            vp.rate(60)

            self.autopilot()
            self.drone.update(self.dt)

            # Verificação estrita de colisões
            for obs in self.obstacles:
                if obs.collides(self.drone.position, self.drone.radius):
                    print("\nCOLISÃO!")
                    self.drone.crashed = True
                    return

            self.log_sensors()
            self.time += self.dt

        print("\nMISSÃO CONCLUÍDA!")


# ============================================================

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
