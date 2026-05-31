"""
Módulo de gerador de mundo.

Define a classe WorldGenerator que cria e configura o ambiente
de simulação incluindo obstáculos, paredes e terreno.
"""

from typing import List
import vpython as vp
from .obstacle import Obstacle


class WorldGenerator:
    """
    Gerencia a criação e configuração do ambiente de simulação.
    
    Responsável por criar todos os elementos do mundo: terreno, paredes
    e obstáculos.
    """

    def __init__(self) -> None:
        """
        Inicializa o gerador de mundo.
        
        Define valores padrão para a posição da parede e lista vazia
        de obstáculos.
        
        Returns:
            None
        """
        self._wall_y: float = 10.0
        self._obstacles: List[Obstacle] = []

    # -------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------

    @property
    def wall_y(self) -> float:
        """
        Obtém a posição Y da parede final.
        
        Returns:
            Valor float da coordenada Y em metros
        """
        return self._wall_y

    @property
    def obstacles(self) -> List[Obstacle]:
        """
        Obtém a lista de obstáculos do mundo.
        
        Returns:
            Lista contendo todos os objetos Obstacle
        """
        return self._obstacles.copy()

    # -------------------------------------------------------
    # SETTERS
    # -------------------------------------------------------

    @wall_y.setter
    def wall_y(self, new_wall_y: float) -> None:
        """
        Define a posição Y da parede final.
        
        Args:
            new_wall_y: Nova coordenada Y em metros
        
        Returns:
            None
        """
        self._wall_y = float(new_wall_y)

    # -------------------------------------------------------
    # SETUP VISUAL
    # -------------------------------------------------------

    def setup_canvas(self) -> None:
        """
        Configura o canvas e câmera do VPython.
        
        Define título da janela, dimensões, cor de fundo e posição
        da câmera para visualização diagonal do ambiente.
        
        Returns:
            None
        """
        vp.canvas(
            title="Drone Simulator - Slalom Perfeito por Fora (Sem Hélices)",
            width=1400,
            height=900,
            background=vp.color.white,
        )

        # Reposiciona a câmera para visualização diagonal de cima
        vp.scene.camera.pos = vp.vector(0, -9, 6)
        vp.scene.camera.axis = vp.vector(0, 9, -5)

    # -------------------------------------------------------
    # GERAÇÃO DO MUNDO
    # -------------------------------------------------------

    def create_ground(self) -> None:
        """
        Cria o terreno (chão) da simulação.
        
        Cria um grande plano verde que serve como solo do ambiente.
        
        Returns:
            None
        """
        vp.box(
            pos=vp.vector(0, 2, -0.1), 
            size=vp.vector(16, 24, 0.2), 
            color=vp.color.green
        )

    def create_wall(self) -> None:
        """
        Cria a parede final (barreira de término).
        
        Cria um plano vermelho na posição Y definida como limite da pista.
        
        Returns:
            None
        """
        vp.box(
            pos=vp.vector(0, self._wall_y, 1),
            size=vp.vector(8, 0.2, 2),
            color=vp.color.red,
        )

    def create_obstacles(self) -> None:
        """
        Cria os obstáculos do trajeto em Slalom.
        
        Cria dois obstáculos estrategicamente posicionados para
        teste de navegação em Slalom.
        
        Returns:
            None
        """
        self._obstacles = [
            Obstacle(
                [-1.2, 0.0, 1],
                [1, 1, 2],
                vp.color.orange,
            ),
            Obstacle(
                [1.2, 4.5, 1],
                [1, 1, 2],
                vp.color.purple,
            ),
        ]

    def generate(self) -> None:
        """
        Gera o mundo completo.
        
        Executa todas as etapas de criação do ambiente em ordem:
        canvas, terreno, parede e obstáculos.
        
        Returns:
            None
        """
        self.setup_canvas()
        self.create_ground()
        self.create_wall()
        self.create_obstacles()

    # -------------------------------------------------------
    # GETTERS DE DADOS
    # -------------------------------------------------------

    def get_obstacles(self) -> List[Obstacle]:
        """
        Retorna a lista de obstáculos do mundo.
        
        Returns:
            Lista contendo todos os objetos Obstacle
        """
        return self._obstacles.copy()

    def get_wall_y(self) -> float:
        """
        Retorna a posição Y da parede final.
        
        Returns:
            Valor float da coordenada Y em metros
        """
        return self._wall_y

