#!/usr/bin/env python3
"""动作客户端节点 - 请求 MoveRobot 动作"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from custom_interfaces.action import MoveRobot


class ActionClientNode(Node):
    def __init__(self):
        super().__init__('action_client_node')

        self._action_client = ActionClient(self, MoveRobot, 'move_robot')

        self.get_logger().info('动作客户端节点已启动')

        self.send_goal()

    def send_goal(self):
        goal = MoveRobot.Goal()
        goal.target_position.x = 5.0
        goal.target_position.y = 10.0
        goal.target_position.z = 0.0
        goal.speed = 2.0

        self.get_logger().info(f'发送目标: position=({goal.target_position.x}, '
                               f'{goal.target_position.y}, {goal.target_position.z}), speed={goal.speed}')

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('目标被拒绝')
            return

        self.get_logger().info('目标被接受，等待结果...')
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback):
        self.get_logger().info(
            f'收到反馈: progress={feedback.feedback.progress*100:.0f}%, '
            f'status={feedback.feedback.status_message}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'收到结果: success={result.success}, message={result.message}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = ActionClientNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()