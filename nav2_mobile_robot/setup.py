from setuptools import find_packages, setup

package_name = "nav2_mobile_robot"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            "share/" + package_name,
            [
                "launch/display.launch.py",
                "launch/gazebo.launch.py",
                "launch/slam.launch.py",
                "launch/map_server.launch.py",
                "launch/amcl.launch.py",
                "launch/navigation.launch.py",
                "launch/scripts.launch.py",
                "urdf/nav2_mobile_robot.xacro",
                "urdf/gazebo_control.xacro",
                "urdf/lidar.xacro",
                "urdf/nav2_mobile_robot_macro.xacro",
                "urdf/odom_plugin.xacro",
                "rviz/rviz.rviz",
                "worlds/comp1.sdf",
                "worlds/competition.sdf",
                "worlds/maze.sdf",
            
                "config/slam.yaml",
                "config/amcl.yaml",
                "config/nav.yaml",
                "map/map.yaml",
                "map/map.pgm",
            ],
        ),
    ],
    install_requires=["setuptools", "visualization_msgs",  "geometry_msgs", "nav_msgs"],
    zip_safe=True,
    maintainer="mohamedrayan73",
    maintainer_email="mohamedrayan71763@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            'localization = nav2_mobile_robot.localization:main',
        'mine_detection = nav2_mobile_robot.mine_detection:main',
        'mission_manager = nav2_mobile_robot.mission_manager:main',
        ],
    },
)
