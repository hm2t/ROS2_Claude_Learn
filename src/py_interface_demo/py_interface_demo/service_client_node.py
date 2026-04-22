#!/usr/bin/env python3
"""服务客户端节点 - 请求 GetRobotInfo 服务"""

import rclpy
from rclpy.node import Node

from custom_interfaces.srv import GetRobotInfo


class ServiceClientNode(Node):
    def __init__(self):
        super().__init__('service_client_node')

        self.client = self.create_client(GetRobotInfo, 'get_robot_info')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务端上线...')

        self.get_logger().info('服务客户端节点已启动')

        self.send_request()

    def send_request(self):
        request = GetRobotInfo.Request()
        request.robot_name = 'robot_001'

        self.get_logger().info(f'发送请求: robot_name={request.robot_name}')

        future = self.client.call_async(request)
        future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(
                f'收到响应: name={response.status.name}, '
                f'battery={response.status.battery_level}, '
                f'position=({response.position.x}, {response.position.y}, {response.position.z})')
        except rclpy.client.ClientException as e:
            self.get_logger().error(f'服务调用失败 (ClientException): {e}')
        except TimeoutError as e:
            self.get_logger().error(f'服务调用超时: {e}')
        except Exception as e:
            self.get_logger().error(f'服务调用失败: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ServiceClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('节点被 KeyboardInterrupt 终止')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()