import vpython as vp
import numpy as np
from drone_sim.drone import Drone
from drone_sim.world import WorldGenerator


class Simulation:
    """
    Gerencia a simulação completa do drone incluindo autopiloto,
    atualização de física e log de sensores.
    """

    def __init__(self):
        """Inicializa a simulação criando o mundo e o drone."""
        # Geração do mundo
        self.world_generator = WorldGenerator()
        self.world_generator.generate()

        self.obstacles = self.world_generator.get_obstacles()
        self.wall_y = self.world_generator.get_wall_y()

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
        """Controla o drone automaticamente através dos estados de voo."""
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
        """Registra os dados dos sensores a cada segundo."""
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
    # LOOP PRINCIPAL
    # -------------------------------------------------------

    def run(self):
        """Executa o loop principal da simulação."""
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
