from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='fertilizer_controller',
            executable='fertilizer_node', 
            name='fertilizer_controller_node',
            output='screen'
        )
    ])
