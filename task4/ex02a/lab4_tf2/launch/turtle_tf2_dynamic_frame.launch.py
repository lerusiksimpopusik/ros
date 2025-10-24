from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'radius', default_value='1.0',
            description='Radius of carrot trajectory.'
        ),
        DeclareLaunchArgument(
            'direction_of_rotation', default_value='1',
            description='Direction of carrot rotation. (1 - clockwise, -1 - counterclockwise)'
        ),
        IncludeLaunchDescription(
            PathJoinSubstitution([
                FindPackageShare('lab4_tf2'), 'launch', 'turtle_tf2.launch.py']),
            launch_arguments={'target_frame': 'carrot'}.items(),
        ),
        Node(
            package='lab4_tf2',
            executable='dynamic_frame_tf2_broadcaster',
            name='dynamic_broadcaster',
            parameters=[
                {'radius': LaunchConfiguration('radius')},
                {'direction_of_rotation': LaunchConfiguration('direction_of_rotation')}
            ]
        ),
    ])