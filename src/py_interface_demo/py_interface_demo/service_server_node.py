#!/usr/bin/env python3
"""服务服务端节点 - 提供 GetRobotInfo 服务"""

import rclpy
from rclpy.node import Node

from custom_interfaces.srv import GetRobotInfo


class ServiceServerNode(Node):
    def __init__(self):
        super().__init__('service_server_node')

        self.srv = self.create_service(
            GetRobotInfo, 'get_robot_info', self.handle_robot_info)

        self.get_logger().info('服务服务端节点已启动，等待请求...')

    def handle_robot_info(self, request, response):
        self.get_logger().info(f'收到请求: robot_name={request.robot_name}')

        response.status.name = request.robot_name
        response.status.is_active = True
        response.status.battery_level = 0.92
        response.position.x = 10.5
        response.position.y = 20.3
        response.position.z = 0.0

        self.get_logger().info('已返回机器人信息')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = ServiceServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()