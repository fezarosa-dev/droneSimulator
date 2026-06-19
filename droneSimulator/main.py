"""
Módulo principal do simulador de drone com ROS 2.

Inicializa e executa o nó ROS 2 de simulação de drone.
"""

import sys
import rclpy
from .drone_simulator_node import DroneSimulatorNode


def main() -> None:
    """
    Função principal que executa o simulador de drone com ROS 2.
    
    Inicializa o ROS 2, cria o nó do simulador e executa o spin.
    
    Returns:
        None
    """
    rclpy.init(args=None)
    
    try:
        # Cria o nó do simulador
        node = DroneSimulatorNode()
        
        # Executa o nó
        rclpy.spin(node)
        
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário")
    except Exception as e:
        print(f"Erro na simulação: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        rclpy.shutdown()


if __name__ == "__main__":
    main()


import signal
import sys

def signal_handler(sig, frame):
    print("\nEncerrando simulador...")
    rclpy.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)