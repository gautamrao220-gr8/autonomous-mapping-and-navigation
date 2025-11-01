from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetLaunchConfiguration, GroupAction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Config argument (linear.yaml by default)
    config_arg = DeclareLaunchArgument(
        'config',
        default_value='linear'
    )
    config_file = SetLaunchConfiguration(
        'config_file',
        [LaunchConfiguration('config'), '.yaml']
    )
    config_file_path = PathJoinSubstitution(
        [FindPackageShare('interactive_marker_twist_server'),
         'config',
         LaunchConfiguration('config_file')]
    )

    # List of robots
    robots = ['robot1', 'robot2', 'robot3', 'robot4']

    robot_groups = []
    for robot in robots:
        group = GroupAction([
            PushRosNamespace(robot),  # namespace per robot
            Node(
                package='interactive_marker_twist_server',
                executable='marker_server',
                name=f'twist_server_node_{robot}',  # unique node name
                parameters=[config_file_path],
                output='screen',
            )
        ])
        robot_groups.append(group)

    ld = LaunchDescription()
    ld.add_action(config_arg)
    ld.add_action(config_file)

    for g in robot_groups:
        ld.add_action(g)

    return ld
