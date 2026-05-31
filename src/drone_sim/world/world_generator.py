import vpython as vp
from .obstacle import Obstacle


class WorldGenerator:
    """
    Gerencia a criação e configuração do ambiente de simulação.
    """

    def __init__(self):
        """Inicializa o gerador de mundo."""
        self.wall_y = 10
        self.obstacles = []

    # -------------------------------------------------------
    # SETUP VISUAL
    # -------------------------------------------------------

    def setup_canvas(self):
        """Configura o canvas e câmera do VPython."""
        vp.canvas(
            title="Drone Simulator - Slalom Perfeito por Fora (Sem Hélices)",
            width=1400,
            height=900,
            background=vp.color.white,
        )

        # Reposiciona a câmera do VPython para olhar o drone de cima em diagonal
        vp.scene.camera.pos = vp.vector(0, -9, 6)
        vp.scene.camera.axis = vp.vector(0, 9, -5)

    # -------------------------------------------------------
    # GERAÇÃO DO MUNDO
    # -------------------------------------------------------

    def create_ground(self):
        """Cria o chão da simulação."""
        vp.box(
            pos=vp.vector(0, 2, -0.1), size=vp.vector(16, 24, 0.2), color=vp.color.green
        )

    def create_wall(self):
        """Cria a parede final."""
        vp.box(
            pos=vp.vector(0, self.wall_y, 1),
            size=vp.vector(8, 0.2, 2),
            color=vp.color.red,
        )

    def create_obstacles(self):
        """Cria os obstáculos do trajeto em Slalom."""
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

    def generate(self):
        """Gera o mundo completo."""
        self.setup_canvas()
        self.create_ground()
        self.create_wall()
        self.create_obstacles()

    def get_obstacles(self):
        """Retorna a lista de obstáculos."""
        return self.obstacles

    def get_wall_y(self):
        """Retorna a posição Y da parede."""
        return self.wall_y
