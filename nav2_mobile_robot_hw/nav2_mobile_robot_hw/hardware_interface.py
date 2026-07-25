#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from std_msgs.msg import Bool


class HardwareInterface(Node):

    def __init__(self):

        super().__init__("hardware_interface")

        # -----------------------------
        # Publishers
        # -----------------------------

        self.odom_pub = self.create_publisher(
            Odometry,
            "/odom",
            10
        )

        self.imu_pub = self.create_publisher(
            Imu,
            "/imu",
            10
        )

        self.gps_pub = self.create_publisher(
            NavSatFix,
            "/gps",
            10
        )

        self.mine_detection_pub = self.create_publisher(
            Bool,
            "/mine_detected",
            10
        )

        # Publish at 10 Hz
        self.timer = self.create_timer(
            0.1,
            self.publish_sensor_data
        )

        self.get_logger().info("Hardware Interface Started")

    # --------------------------------------------------

    def publish_sensor_data(self):

        # Create ROS messages

        odom_msg = Odometry()
        imu_msg = Imu()
        gps_msg = NavSatFix()
        mine_msg = Bool()
        now = self.get_clock().now().to_msg()
        # --------------------------------------------
        # Fake sensor values (replace later with ESP32)
        # --------------------------------------------

        # Odometry
        odom_msg.header.stamp = now
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"

        odom_msg.pose.pose.position.x = 2.5
        odom_msg.pose.pose.position.y = 1.3
        odom_msg.pose.pose.position.z = 0.0

        odom_msg.pose.pose.orientation.x = 0.0
        odom_msg.pose.pose.orientation.y = 0.0
        odom_msg.pose.pose.orientation.z = 0.0
        odom_msg.pose.pose.orientation.w = 1.0

        # GPS
        gps_msg.header.stamp = now
        gps_msg.latitude = 30.0156
        gps_msg.longitude = 31.4421
        gps_msg.altitude = 0.0

        # IMU
        imu_msg.header.stamp = now
        imu_msg.orientation.x = 0.0
        imu_msg.orientation.y = 0.0
        imu_msg.orientation.z = 0.0
        imu_msg.orientation.w = 1.0

        # Metal detector

        mine_msg.data = False

        # --------------------------------------------
        # Publish
        # --------------------------------------------

        self.odom_pub.publish(odom_msg)
        self.imu_pub.publish(imu_msg)
        self.gps_pub.publish(gps_msg)
        self.mine_detection_pub.publish(mine_msg)

        # Print status

        self.get_logger().info(
            f"Published -> "
            f"x={odom_msg.pose.pose.position.x:.2f}, "
            f"y={odom_msg.pose.pose.position.y:.2f}, "
            f"GPS=({gps_msg.latitude:.5f}, {gps_msg.longitude:.5f}), "
            f"Mine={mine_msg.data}"
        )


# --------------------------------------------------

def main(args=None):

    rclpy.init(args=args)

    node = HardwareInterface()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

        


        