from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class Server(Node):
    def __init__(self):
        super().__init__('server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.server_callback)

    def server_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Request: {request.a} + {request.b} = {response.sum}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
