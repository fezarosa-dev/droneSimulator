from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Gera a descrição de launch para o simulador de drone.
    
    Cria um nó do simulador que publica dados de sensores em tópicos ROS 2.
    
    Returns:
        LaunchDescription com o nó do simulador configurado
    """
    
    # Nó do simulador
    drone_simulator_node = Node(
        package='droneSimulator',
        executable='drone_simulator',
        name='drone_simulator',
        output='screen',
        emulate_tty=True,
    )
    
    return LaunchDescription([
        drone_simulator_node,
    ])
