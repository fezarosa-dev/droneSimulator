import vpython as vp
import numpy as np


class Obstacle:
    """
    Representa um obstáculo na simulação.
    """

    def __init__(self, pos, size, color):
        """
        Inicializa um obstáculo.
        
        Args:
            pos: Posição [x, y, z]
            size: Tamanho [width, height, depth]
            color: Cor do obstáculo (vpython color)
        """
        self.pos = np.array(pos, dtype=float)
        self.size = np.array(size, dtype=float)
        self.visual = vp.box(pos=vp.vector(*pos), size=vp.vector(*size), color=color)

    def collides(self, drone_pos, radius):
        """
        Verifica se o drone colidiu com este obstáculo.
        
        Args:
            drone_pos: Posição do drone [x, y, z]
            radius: Raio do drone
            
        Returns:
            True se houve colisão, False caso contrário
        """
        delta = np.abs(drone_pos - self.pos)

        return (
            delta[0] <= self.size[0] / 2 + radius
            and delta[1] <= self.size[1] / 2 + radius
            and delta[2] <= self.size[2] / 2 + radius
        )
