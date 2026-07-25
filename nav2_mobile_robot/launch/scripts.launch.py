from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    localization = Node(
        package="nav2_mobile_robot",
        executable="localization",
        name="localization",
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    mine_detection = Node(
        package="nav2_mobile_robot",
        executable="mine_detection",
        name="mine_detection",
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    mission_manager = Node(
        package="nav2_mobile_robot",
        executable="mission_manager",
        name="mission_manager",
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    return LaunchDescription([
        localization,
        mine_detection,
        mission_manager,
    ])