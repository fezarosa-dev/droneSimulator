"""
Nó ROS 2 para simulação de drone.

Gerencia a simulação do drone e publica dados de sensores em tópicos ROS 2.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, TwistStamped
from sensor_msgs.msg import Imu, Range
from std_msgs.msg import String, Float32
import numpy as np

from .simulation import Simulation


class DroneSimulatorNode(Node):
    """
    Nó ROS 2 para simular um drone com publicação de sensores.
    
    Publica dados de:
    - GPS (PoseStamped)
    - IMU (Imu)
    - LIDAR (Range)
    - Estado da missão (String)
    - Tempo de simulação (Float32)
    - Velocidade (TwistStamped)
    """

    def __init__(self):
        """
        Inicializa o nó ROS 2 e a simulação do drone.
        
        Returns:
            None
        """
        super().__init__('drone_simulator')
        
        # Inicializa simulação
        self._simulation: Simulation = Simulation()
        
        # Taxa de execução (60 Hz)
        self._dt: float = 0.02
        self._frame_count: int = 0
        
        # Criação de publishers
        self._gps_pub = self.create_publisher(
            PoseStamped, 
            '/drone/gps', 
            10
        )
        self._imu_pub = self.create_publisher(
            Imu, 
            '/drone/imu', 
            10
        )
        self._lidar_pub = self.create_publisher(
            Range, 
            '/drone/lidar', 
            10
        )
        self._state_pub = self.create_publisher(
            String, 
            '/drone/state', 
            10
        )
        self._time_pub = self.create_publisher(
            Float32, 
            '/drone/time', 
            10
        )
        self._velocity_pub = self.create_publisher(
            TwistStamped, 
            '/drone/velocity', 
            10
        )
        
        # Timer para update da simulação (60 Hz)
        self._timer = self.create_timer(self._dt, self._simulation_step)
        
        self.get_logger().info("Drone Simulator Node iniciado!")
        self.get_logger().info("Iniciando simulação...")
    
    def _simulation_step(self) -> None:
        """
        Executa um passo da simulação e publica dados dos sensores.
        
        Returns:
            None
        """
        try:
            # Atualiza autopiloto
            self._simulation._autopilot.update(
                self._simulation._drone,
                self._simulation._obstacles,
                self._simulation._wall_y,
                self._dt
            )
            
            # Atualiza física do drone
            self._simulation._drone.update(self._dt)
            
            # Verifica colisão
            if self._simulation._check_collisions():
                self.get_logger().warn("COLISÃO DETECTADA!")
                self._simulation._drone.crashed = True
                self._cancel_timer()
                return
            
            # Publica dados dos sensores
            self._publish_sensors()
            
            # Atualiza tempo
            self._simulation._time += self._dt
            self._frame_count += 1
            
            # Log a cada segundo
            self._simulation.log_sensors()
            
            # Verifica se missão foi concluída
            if self._simulation._autopilot.state == "DONE":
                self.get_logger().info("Missão concluída!")
                self._cancel_timer()
                
        except Exception as e:
            self.get_logger().error(f"Erro na simulação: {str(e)}")
            self._cancel_timer()
    
    def _publish_sensors(self) -> None:
        """
        Publica dados dos sensores do drone em tópicos ROS 2.
        
        Returns:
            None
        """
        timestamp = self.get_clock().now().to_msg()
        
        # GPS
        self._publish_gps(timestamp)
        
        # IMU
        self._publish_imu(timestamp)
        
        # LIDAR
        self._publish_lidar(timestamp)
        
        # Estado
        self._publish_state()
        
        # Tempo
        self._publish_time()
        
        # Velocidade
        self._publish_velocity(timestamp)
    
    def _publish_gps(self, timestamp) -> None:
        """
        Publica dados GPS (posição).
        
        Args:
            timestamp: Timestamp da mensagem
        
        Returns:
            None
        """
        gps_data = self._simulation._drone.gps()
        
        pose_msg = PoseStamped()
        pose_msg.header.stamp = timestamp
        pose_msg.header.frame_id = "world"
        
        pose_msg.pose.position.x = float(gps_data[0])
        pose_msg.pose.position.y = float(gps_data[1])
        pose_msg.pose.position.z = float(gps_data[2])
        
        # Orientação padrão (sem rotação)
        pose_msg.pose.orientation.x = 0.0
        pose_msg.pose.orientation.y = 0.0
        pose_msg.pose.orientation.z = 0.0
        pose_msg.pose.orientation.w = 1.0
        
        self._gps_pub.publish(pose_msg)
    
    def _publish_imu(self, timestamp) -> None:
        """
        Publica dados IMU (orientação e aceleração).
        
        Args:
            timestamp: Timestamp da mensagem
        
        Returns:
            None
        """
        imu_data = self._simulation._drone.imu()
        
        imu_msg = Imu()
        imu_msg.header.stamp = timestamp
        imu_msg.header.frame_id = "drone_link"
        
        # Orientação (da aceleração angular)
        imu_msg.angular_velocity.x = float(imu_data['roll'])
        imu_msg.angular_velocity.y = float(imu_data['pitch'])
        imu_msg.angular_velocity.z = float(imu_data['yaw'])
        
        # Aceleração linear
        velocity = self._simulation._drone.velocity
        imu_msg.linear_acceleration.x = velocity[0]
        imu_msg.linear_acceleration.y = velocity[1]
        imu_msg.linear_acceleration.z = velocity[2] - 9.81  # Subtraindo gravidade
        
        self._imu_pub.publish(imu_msg)
    
    def _publish_lidar(self, timestamp) -> None:
        """
        Publica dados LIDAR (altitude/distância do solo).
        
        Args:
            timestamp: Timestamp da mensagem
        
        Returns:
            None
        """
        lidar_data = self._simulation._drone.lidar()
        
        range_msg = Range()
        range_msg.header.stamp = timestamp
        range_msg.header.frame_id = "lidar_link"
        
        range_msg.radiation_type = Range.INFRARED
        range_msg.field_of_view = 0.5236  # 30 graus em radianos
        range_msg.min_range = 0.0
        range_msg.max_range = 100.0
        range_msg.range = float(lidar_data)
        
        self._lidar_pub.publish(range_msg)
    
    def _publish_state(self) -> None:
        """
        Publica o estado atual da missão.
        
        Returns:
            None
        """
        state_msg = String()
        state_msg.data = self._simulation._autopilot.state
        
        self._state_pub.publish(state_msg)
    
    def _publish_time(self) -> None:
        """
        Publica o tempo da simulação.
        
        Returns:
            None
        """
        time_msg = Float32()
        time_msg.data = float(self._simulation._time)
        
        self._time_pub.publish(time_msg)
    
    def _publish_velocity(self, timestamp) -> None:
        """
        Publica a velocidade do drone.
        
        Args:
            timestamp: Timestamp da mensagem
        
        Returns:
            None
        """
        velocity = self._simulation._drone.velocity
        
        twist_msg = TwistStamped()
        twist_msg.header.stamp = timestamp
        twist_msg.header.frame_id = "drone_link"
        
        twist_msg.twist.linear.x = float(velocity[0])
        twist_msg.twist.linear.y = float(velocity[1])
        twist_msg.twist.linear.z = float(velocity[2])
        
        self._velocity_pub.publish(twist_msg)
    
    def _cancel_timer(self) -> None:
        """
        Cancela o timer da simulação.
        
        Returns:
            None
        """
        self._timer.cancel()
