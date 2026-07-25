#!/usr/bin/env python3
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import math
import rclpy
from rclpy.node import Node
from tf2_ros import Buffer
from tf2_ros import TransformListener


from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose2D



class Localization(Node):

    def __init__(self):
        super().__init__("localization")
        
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.pose_pub = self.create_publisher(
            Pose2D,
            "/robot_pose",
            10
        )
        self.marker_pub = self.create_publisher(
            Marker,
            "/robot_marker",
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.publish_pose
        )

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        
        q = msg.pose.pose.orientation

        self.theta = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

    def publish_pose(self):
        msg = Pose2D()
        msg.x = self.x
        msg.y = self.y
        msg.theta = self.theta
        self.pose_pub.publish(msg)
        self.publish_marker()
        print("----------------------")
        print(f"x = {msg.x:.3f}")
        print(f"y = {msg.y:.3f}")
        print(f"theta = {math.degrees(msg.theta):.1f} deg")

    def publish_marker(self):

        marker = Marker()

        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "robot"
        marker.id = 0

        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        marker.pose.position.x = self.x
        marker.pose.position.y = self.y
        marker.pose.position.z = 0.1

        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = math.sin(self.theta / 2.0)
        marker.pose.orientation.w = math.cos(self.theta / 2.0)

        marker.scale.x = 0.5      # Arrow length
        marker.scale.y = 0.10     # Arrow width
        marker.scale.z = 0.10     # Arrow height

        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        self.marker_pub.publish(marker)
def main(args=None):
    rclpy.init(args=args)
    node = Localization()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()