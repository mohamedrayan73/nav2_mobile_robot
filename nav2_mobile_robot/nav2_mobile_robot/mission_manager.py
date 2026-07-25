#!/usr/bin/env python3

import math
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
class MissionManager(Node):

    def __init__(self):
        super().__init__("mission_manager")

        self.mine_list = []
        self.mine_counter = 0
        self.minimum_distance = 0.50 # 50cm radius filter

        # Path to save the final results
        self.save_path = os.path.expanduser("~/robot_ws/src/nav2_mobile_robot/detected_mines.csv")

        self.mine_sub = self.create_subscription(
            Pose2D,
            "/mine_location",
            self.mine_callback,
            10
        )

        self.get_logger().info(f"Mission Manager Started. Data will be saved to: {self.save_path}")

    def mine_callback(self, msg):
        x = msg.x
        y = msg.y

        # Check if this mine is already in our list (distance check)
        for mine in self.mine_list:
            distance = math.sqrt((mine[0]-x)**2 + (mine[1]-y)**2)
            if distance < self.minimum_distance:
                # We already know about this mine! Skip it.
                return

        # New Mine Found!
        self.mine_counter += 1
        self.mine_list.append((x, y))

        # --- LOGGING ---
        self.get_logger().info("========================")
        self.get_logger().info(f"NEW MINE DETECTED! (# {self.mine_counter})")
        self.get_logger().info(f"Location: X={x:.2f}, Y={y:.2f}")
        self.get_logger().info("========================")

        # Print the current summary table
        print("\n--- CURRENT MINE MAP ---")
        for i, mine in enumerate(self.mine_list):
            print(f"Mine {i+1}: ({mine[0]:.2f}, {mine[1]:.2f})")
        
        # Save to file every time we find a new one (persistent memory)
        self.save_mines_to_file()

    def save_mines_to_file(self):
        try:
            with open(self.save_path, "w") as f:
                f.write("Mine_ID,X,Y\n") # Header
                for i, mine in enumerate(self.mine_list):
                    f.write(f"{i+1},{mine[0]:.4f},{mine[1]:.4f}\n")
        except Exception as e:
            self.get_logger().error(f"Could not save file: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = MissionManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Mission Stopped. Final report is in your CSV file.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()