#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from std_msgs.msg import Bool, Int32
from visualization_msgs.msg import Marker, MarkerArray


class MineDetection(Node):

    def __init__(self):

        super().__init__("mine_detection")

        # -----------------------------
        # Current robot pose
        # -----------------------------
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Prevent duplicate detections
        self.mine_already_detected = False

        # Number of mines found
        self.mine_count = 0

        # Store RViz markers
        self.mine_markers = MarkerArray()

        # -----------------------------
        # Subscribers
        # -----------------------------
        self.pose_sub = self.create_subscription(
            Pose2D,
            "/robot_pose",
            self.pose_callback,
            10
        )

        self.detector_sub = self.create_subscription(
            Bool,
            "/mine_detected",
            self.detector_callback,
            10
        )

        # -----------------------------
        # Publishers
        # -----------------------------
        self.mine_pub = self.create_publisher(
            Pose2D,
            "/mine_location",
            10
        )

        self.marker_pub = self.create_publisher(
            MarkerArray,
            "/mine_markers",
            10
        )

        self.count_pub = self.create_publisher(
            Int32,
            "/mine_count",
            10
        )

        self.get_logger().info("Mine Detection Node Started")

    # ------------------------------------------------

    def pose_callback(self, msg):

        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    # ------------------------------------------------

    def detector_callback(self, msg):

        if msg.data and not self.mine_already_detected:

            ##############################
            # Publish Mine Pose
            ##############################

            mine = Pose2D()

            mine.x = self.x
            mine.y = self.y
            mine.theta = self.theta

            self.mine_pub.publish(mine)

            ##############################
            # Increase Mine Counter
            ##############################

            self.mine_count += 1

            counter = Int32()
            counter.data = self.mine_count

            self.count_pub.publish(counter)

            ##############################
            # Create RViz Marker
            ##############################

            marker = Marker()

            marker.header.frame_id = "map"
            marker.header.stamp = self.get_clock().now().to_msg()

            marker.ns = "mines"
            marker.id = self.mine_count

            marker.type = Marker.SPHERE
            marker.action = Marker.ADD

            marker.pose.position.x = self.x
            marker.pose.position.y = self.y
            marker.pose.position.z = 0.05

            marker.pose.orientation.w = 1.0

            marker.scale.x = 0.07
            marker.scale.y = 0.07
            marker.scale.z = 0.07

            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            self.mine_markers.markers.append(marker)

            self.marker_pub.publish(self.mine_markers)

            ##############################
            # Print Information
            ##############################

            self.get_logger().info("-----------------------------------")
            self.get_logger().info(f"Mine #{self.mine_count}")
            self.get_logger().info(f"X = {self.x:.2f}")
            self.get_logger().info(f"Y = {self.y:.2f}")
            self.get_logger().info(f"Theta = {self.theta:.2f}")

            self.mine_already_detected = True

        elif not msg.data:

            self.mine_already_detected = False


def main(args=None):

    rclpy.init(args=args)

    node = MineDetection()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()