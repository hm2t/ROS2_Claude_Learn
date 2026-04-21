#!/usr/bin/env python3
"""发布者节点 - 发布 RobotStatus 和 Position 消息"""

import rclpy
from rclpy.node import Node

from custom_interfaces.msg import RobotStatus, Position


class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')

        self.robot_status_pub = self.create_publisher(
            RobotStatus, 'robot_status', 10)
        self.position_pub = self.create_publisher(Position, 'position', 10)

        self.status_timer = self.create_timer(1.0, self.publish_status)
        self.position_timer = self.create_timer(0.5, self.publish_position)

        self.get_logger().info('发布者节点已启动')

    def publish_status(self):
        msg = RobotStatus()
        msg.name = 'robot_001'
        msg.is_active = True
        msg.battery_level = 0.85
        self.robot_status_pub.publish(msg)
        self.get_logger().info(f'发布 RobotStatus: name={msg.name}, battery={msg.battery_level}')

    def publish_position(self):
        msg = Position()
        msg.x = 1.0
        msg.y = 2.0
        msg.z = 0.0
        self.position_pub.publish(msg)
        self.get_logger().info(f'发布 Position: x={msg.x}, y={msg.y}, z={msg.z}')


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()