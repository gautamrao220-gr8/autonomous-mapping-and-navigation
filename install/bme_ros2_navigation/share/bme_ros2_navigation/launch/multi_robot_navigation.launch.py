import os
from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Package directories
    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')
    interactive_pkg = get_package_share_directory('interactive_marker_twist_server')

    os.environ["GZ_SIM_RESOURCE_PATH"] += os.pathsep + os.path.split(pkg_bme_ros2_navigation)[0]

    # Common launch args
    rviz_arg = DeclareLaunchArgument('rviz', default_value='true')
    rviz_config_arg = DeclareLaunchArgument('rviz_config', default_value='navigation.rviz')
    sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='True')

    # Updated Config & map paths to match single-robot navigation launch
    localization_params_path = os.path.join(pkg_bme_ros2_navigation, 'config', 'amcl_localization.yaml')
    navigation_params_path = os.path.join(pkg_bme_ros2_navigation, 'config', 'navigation.yaml')
    map_file_path = os.path.join(pkg_bme_ros2_navigation, 'maps', 'my_map.yaml')  # Same prebuilt map
    marker_config_path = os.path.join(interactive_pkg, 'config', 'planar.yaml')

    # RViz (single instance)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', PathJoinSubstitution([pkg_bme_ros2_navigation, 'rviz', LaunchConfiguration('rviz_config')])],
        condition=IfCondition(LaunchConfiguration('rviz')),
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen'
    )

    # Robot definitions
    robots = [
        {'name': 'robot1', 'x': 2.0, 'y': 0.0, 'yaw': 0.0},
        {'name': 'robot2', 'x': 4.0, 'y': 0.0, 'yaw': 0.0},
        {'name': 'robot3', 'x': 2.0, 'y': 2.0, 'yaw': 0.0},
        {'name': 'robot4', 'x': 4.0, 'y': 2.0, 'yaw': 0.0},
    ]

    localization_launch = os.path.join(nav2_bringup_dir, 'launch', 'localization_launch.py')
    navigation_launch = os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')

    robot_groups = []
    for robot in robots:
        ns = robot['name']

        group = GroupAction([
            PushRosNamespace(ns),

            # Nav2 Localization (AMCL)
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(localization_launch),
                launch_arguments={
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'params_file': localization_params_path,
                    'map': map_file_path,  # Same prebuilt map
                    'namespace': ns,
                }.items()
            ),

            # Nav2 Navigation
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(navigation_launch),
                launch_arguments={
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'params_file': navigation_params_path,
                    'namespace': ns,
                }.items()
            ),

            # Initial Pose Publisher (Python node)
            Node(
                package='bme_ros2_navigation_py',
                executable='publish_initial_pose',
                name=f'initial_pose_publisher_{ns}',
                output='screen',
                parameters=[{
                    'namespace': ns,
                    'x': robot['x'],
                    'y': robot['y'],
                    'yaw': robot['yaw'],
                    'use_sim_time': True
                }]
            ),
        ])
        robot_groups.append(group)

    # Interactive Marker Twist Server
    interactive_marker_node = Node(
        package='interactive_marker_twist_server',
        executable='marker_server',
        name='interactive_goal_server',
        parameters=[{
            'config': marker_config_path,
            'use_sim_time': True
        }],
        output='screen'
    )

    # Assemble final launch description
    ld = LaunchDescription()
    ld.add_action(rviz_arg)
    ld.add_action(rviz_config_arg)
    ld.add_action(sim_time_arg)
    ld.add_action(rviz_node)

    for g in robot_groups:
        ld.add_action(g)

    ld.add_action(interactive_marker_node)

    return ld
