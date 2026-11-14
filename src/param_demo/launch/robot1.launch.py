
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    return LaunchDescription([

        DeclareLaunchArgument(
            'speed',
            default_value='0.6',
            description='Robot speed'
        ),

        DeclareLaunchArgument(
            'operating_mode',
            default_value='manual',
            description='Robot operating mode'
        ),

        DeclareLaunchArgument(
            'enabled',
            default_value='true',
            description='Enable status publishing'
        ),

        DeclareLaunchArgument(
                    'enabled',
                    default_value='true',
                    description='Enable status publishing'
        ),
        DeclareLaunchArgument(
            'robot_namespace',
            default_value='robot1',
            description='Namespace for the robot'
        ),

        Node(
            package='param_demo',
            executable='param_mover',
            name='robot_controller',
            namespace=LaunchConfiguration('robot_namespace'),

            parameters=[{
                'speed': ParameterValue(
                    LaunchConfiguration('speed'),
                    value_type=float
                ),

                'operating_mode': LaunchConfiguration(
                    'operating_mode'
                ),

                'turn_rate': ParameterValue(
                    LaunchConfiguration('turn_rate'),
                    value_type=float
                ),

                'enabled': ParameterValue(
                    LaunchConfiguration('enabled'),
                    value_type=bool
                )
            }],

            remappings=[
                ('Robot_status', 'status')
            ]
        )
    ])
