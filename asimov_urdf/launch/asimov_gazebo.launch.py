import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('asimov_urdf')
    urdf_file = os.path.join(pkg, 'asimov_urdf', 'asimov_urdf.urdf')
    world = os.path.join(pkg, 'worlds', 'asimov_world.sdf')
    with open(urdf_file) as f:
        robot_description = f.read()

    # lets Gazebo resolve package://asimov_urdf/meshes/...
    set_res = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.dirname(pkg))

    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items())

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               parameters=[{'robot_description': robot_description,
                            'use_sim_time': True}], output='screen')

    spawn = Node(package='ros_gz_sim', executable='create',
                 arguments=['-world', 'asimov_world', '-file', urdf_file,
                            '-name', 'asimov_bot', '-x', '0', '-y', '0', '-z', '0.2'],
                 output='screen')

    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                  arguments=[
                      '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                      '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                      '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                      '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                      '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
                      '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                      '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
                  ],
                  parameters=[{'use_sim_time': True}], output='screen')

    return LaunchDescription([set_res, gz, rsp, spawn, bridge])