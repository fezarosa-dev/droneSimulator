from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'droneSimulator'

setup(
    name=package_name,
    version='2.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
    ],
    install_requires=[
        'setuptools',
        'numpy==2.4.3',
        'vpython==7.6.5',
        'rclpy',
        'geometry_msgs',
        'sensor_msgs',
        'std_msgs',
    ],
    zip_safe=True,
    maintainer='zanoni',
    maintainer_email='fezarosa.dev@gmail.com',
    description='Simulador de drone com autopiloto e integração ROS 2',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'drone_simulator = droneSimulator.main:main',
        ],
    },
)