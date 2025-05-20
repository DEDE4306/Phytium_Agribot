from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    robot_pkg = get_package_share_directory('turn_on_wheeltec_robot')
    nav_pkg = get_package_share_directory('wheeltec_nav2')
    crop_pkg = get_package_share_directory('crop_detector')
    fert_pkg = get_package_share_directory('fertilizer_controller')
    master_pkg = get_package_share_directory('agri_master_controller')

    return LaunchDescription([
        # 启动底盘
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(robot_pkg, 'launch', 'turn_on_wheeltec_robot.launch.py')
            )
        ),
        # 启动相机
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(robot_pkg, 'launch', 'wheeltec_camera.launch.py')
            )
        ),
        # 启动雷达
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(robot_pkg, 'launch', 'wheeltec_lidar.launch.py')
            )
        ),
        # 启动导航
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav_pkg, 'launch', 'wheeltec_nav2.launch.py')
            )
        ),
        # 启动作物检测节点
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(crop_pkg, 'launch', 'crop_detector.launch.py')
            )
        ),
        # 启动施肥控制节点
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(fert_pkg, 'launch', 'fertilizer_controller.launch.py')
            )
        ),
    ])
