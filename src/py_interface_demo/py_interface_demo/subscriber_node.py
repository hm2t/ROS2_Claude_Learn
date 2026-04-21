#!/usr/bin/env python3
"""订阅者节点 - 订阅 RobotStatus 和 Position 消息"""

import rclpy
from rclpy.node import Node

from custom_interfaces.msg import RobotStatus, Position


class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')

        self.status_sub = self.create_subscription(
            RobotStatus, 'robot_status', self.status_callback, 10)
        self.position_sub = self.create_subscription(
            Position, 'position', self.position_callback, 10)

        self.get_logger().info('订阅者节点已启动')

    def status_callback(self, msg):
        self.get_logger().info(
            f'接收 RobotStatus: name={msg.name}, is_active={msg.is_active}, battery={msg.battery_level}')

    def position_callback(self, msg):
        self.get_logger().info(f'接收 Position: x={msg.x}, y={msg.y}, z={msg.z}')


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()