from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='crop_detector',
            executable='crop_detector_node', 
            name='crop_detector_node',
            output='screen'
        )
    ])
