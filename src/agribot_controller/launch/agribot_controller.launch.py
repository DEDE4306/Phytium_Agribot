from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='agribot_controller',
            executable='agribot_controller',
            output="screen",
            parameters=['config/controller_params.yaml']
        )
    ])