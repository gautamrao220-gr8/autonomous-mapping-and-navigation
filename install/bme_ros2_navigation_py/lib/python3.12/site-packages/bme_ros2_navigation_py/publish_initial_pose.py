#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
import math

class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')
        # Parameters
        self.declare_parameter('namespace', 'robot1')
        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)
        self.declare_parameter('use_sim_time', True)

        ns = self.get_parameter('namespace').get_parameter_value().string_value
        x = self.get_parameter('x').get_parameter_value().double_value
        y = self.get_parameter('y').get_parameter_value().double_value
        yaw = self.get_parameter('yaw').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(PoseWithCovarianceStamped, f'/{ns}/initialpose', 10)

        # Publish once
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(yaw / 2.0)
        msg.pose.covariance = [0.0]*36

        self.publisher_.publish(msg)
        self.get_logger().info(f'Published initial pose for {ns} at ({x},{y},{yaw})')


def main(args=None):
    rclpy.init(args=args)
    node = InitialPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
