import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory

from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        [get_package_share_directory('interactive_marker_twist_server'),
         '/launch/multi_robot_marker.launch.py']
    )
)


def generate_launch_description():
    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    gazebo_models_path, _ = os.path.split(pkg_bme_ros2_navigation)
    os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + gazebo_models_path

    world = 'home.sdf'
    model = 'mogi_bot.urdf'
    use_sim_time = True

    # Robot spawn positions
    spawn_positions = [
        {'name': 'robot1', 'x': '2.0', 'y': '0.0', 'yaw': '0.0'},
        {'name': 'robot2', 'x': '4.0', 'y': '0.0', 'yaw': '0.0'},
        {'name': 'robot3', 'x': '2.0', 'y': '2.0', 'yaw': '0.0'},
        {'name': 'robot4', 'x': '4.0', 'y': '2.0', 'yaw': '0.0'},
    ]

    # Include world
    world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_bme_ros2_navigation, 'launch', 'world.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    urdf_file_path = PathJoinSubstitution([
        pkg_bme_ros2_navigation,
        "urdf",
        model
    ])

    gz_bridge_params_path = os.path.join(
        get_package_share_directory('bme_ros2_navigation'),
        'config',
        'gz_bridge.yaml'
    )

    ekf_config_path = os.path.join(
        pkg_bme_ros2_navigation,
        'config',
        'ekf.yaml'
    )

    # Define one group per robot (namespace isolation)
    robot_groups = []
    for robot in spawn_positions:
        ns = robot['name']
        x, y, yaw = robot['x'], robot['y'], robot['yaw']

        group = GroupAction([
            PushRosNamespace(ns),

            # Spawn robot in Gazebo
            Node(
                package="ros_gz_sim",
                executable="create",
                arguments=[
                    "-name", ns,
                    "-topic", "robot_description",
                    "-x", x, "-y", y, "-z", "0.1", "-Y", yaw
                ],
                output="screen",
                parameters=[{'use_sim_time': use_sim_time}]
            ),

            # Robot state publisher
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
                parameters=[{
                    'robot_description': Command(['xacro ', urdf_file_path]),
                    'use_sim_time': use_sim_time
                }]
            ),

            # EKF localization
            Node(
                package='robot_localization',
                executable='ekf_node',
                name='ekf_filter_node',
                output='screen',
                parameters=[ekf_config_path, {'use_sim_time': use_sim_time}]
            ),

            # Bridges
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                arguments=['--ros-args', '-p', f'config_file:={gz_bridge_params_path}'],
                output="screen",
                parameters=[{'use_sim_time': use_sim_time}]
            ),
        ])

        robot_groups.append(group)

    ld = LaunchDescription()
    ld.add_action(world_launch)
    for g in robot_groups:
        ld.add_action(g)

    return ld
