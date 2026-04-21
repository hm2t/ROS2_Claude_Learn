from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class Client(Node):
    def __init__(self):
        super().__init__('client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    node = Client()
    node.send_request(5, 3)
    while rclpy.ok():
        rclpy.spin_once(node)
        if hasattr(node, 'future') and node.future.done():
            try:
                response = node.future.result()
                node.get_logger().info(f'Result: {response.sum}')
            except Exception as e:
                node.get_logger().error(f'Service call failed: {e}')
            break
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
