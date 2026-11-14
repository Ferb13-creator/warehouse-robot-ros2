from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='param_demo',
            executable='param_mover',
            name='robot_controller'
        )
    ])    