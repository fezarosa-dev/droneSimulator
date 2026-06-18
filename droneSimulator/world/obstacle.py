"""
Módulo de obstáculos da simulação.

Define a classe Obstacle que representa objetos estáticos no ambiente
de simulação com detecção de colisão.
"""

from typing import Tuple
import vpython as vp
import numpy as np


class Obstacle:
    """
    Representa um obstáculo estático na simulação.
    
    Um obstáculo é um objeto cúbico com posição, tamanho e cor definidos,
    e fornece detecção de colisão com o drone.
    """

    def __init__(self, pos: Tuple[float, float, float], 
                 size: Tuple[float, float, float], 
                 color: vp.vector) -> None:
        """
        Inicializa um obstáculo com posição, tamanho e cor.
        
        Args:
            pos: Posição do obstáculo no espaço 3D [x, y, z]
            size: Dimensões do obstáculo [width, height, depth]
            color: Cor do obstáculo usando cores VPython (ex: vp.color.orange)
        
        Returns:
            None
        """
        self._pos: np.ndarray = np.array(pos, dtype=float)
        self._size: np.ndarray = np.array(size, dtype=float)
        self._visual: vp.box = vp.box(
            pos=vp.vector(*pos), 
            size=vp.vector(*size), 
            color=color
        )

    # -------------------------------------------------------
    # GETTERS
    # -------------------------------------------------------

    @property
    def pos(self) -> np.ndarray:
        """
        Obtém a posição atual do obstáculo.
        
        Returns:
            Array numpy contendo as coordenadas [x, y, z]
        """
        return self._pos

    @property
    def size(self) -> np.ndarray:
        """
        Obtém o tamanho do obstáculo.
        
        Returns:
            Array numpy contendo as dimensões [width, height, depth]
        """
        return self._size

    @property
    def visual(self) -> vp.box:
        """
        Obtém o objeto visual VPython do obstáculo.
        
        Returns:
            Objeto vp.box que representa o obstáculo visualmente
        """
        return self._visual

    # -------------------------------------------------------
    # SETTERS
    # -------------------------------------------------------

    @pos.setter
    def pos(self, new_pos: Tuple[float, float, float]) -> None:
        """
        Define uma nova posição para o obstáculo.
        
        Args:
            new_pos: Nova posição [x, y, z]
        
        Returns:
            None
        """
        self._pos = np.array(new_pos, dtype=float)
        self._visual.pos = vp.vector(*new_pos)

    # -------------------------------------------------------
    # MÉTODOS
    # -------------------------------------------------------

    def collides(self, drone_pos: np.ndarray, radius: float) -> bool:
        """
        Verifica se o drone colidiu com este obstáculo.
        
        Utiliza cálculo AABB (Axis-Aligned Bounding Box) para determinar
        se a esfera do drone intersecta com o cubo do obstáculo.
        
        Args:
            drone_pos: Posição do drone [x, y, z]
            radius: Raio de colisão do drone
        
        Returns:
            True se houve colisão, False caso contrário
        """
        delta: np.ndarray = np.abs(drone_pos - self._pos)

        collision_detected: bool = (
            delta[0] <= self._size[0] / 2 + radius
            and delta[1] <= self._size[1] / 2 + radius
            and delta[2] <= self._size[2] / 2 + radius
        )

        return collision_detected

