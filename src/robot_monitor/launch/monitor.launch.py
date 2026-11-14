import os 
from ament_index_python.packages import get_package_share_directory 
from launch import LaunchDescription 
from launch.actions import DeclareLaunchArgument 
from launch.substitutions import LaunchConfiguration 
from launch_ros.actions import Node 
from launch_ros.parameter_descriptions import ParameterValue 

def generate_launch_description(): 
    config = os.path.join(
         get_package_share_directory('robot_monitor'),
         'config', 'monitor_params.yaml')
    return LaunchDescription([
        DeclareLaunchArgument(
            'auto_recharge',             
            default_value='false',             
            description='Let the monitor recharge the robot automatically'),

        Node(
            
            package='robot_monitor',             
            executable='sensor_node',             
            name='sensor_node',             
            parameters=[config],             
            output='screen'),

        Node(
            
            package='robot_monitor',
            executable='monitor_node',             
            name='monitor_node',             
            parameters=[
                config,                 
                {'auto_recharge': ParameterValue(
                    LaunchConfiguration('auto_recharge'),

value_type=bool)},
             ],
              output='screen'),
    ])          