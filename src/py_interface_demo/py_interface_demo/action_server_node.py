#!/usr/bin/env python3
"""动作服务端节点 - 提供 MoveRobot 动作服务"""

import threading
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from custom_interfaces.action import MoveRobot


class ActionServerNode(Node):
    def __init__(self):
        super().__init__('action_server_node')

        self._action_server = ActionServer(
            self, MoveRobot, 'move_robot', self.execute_callback)

        self.get_logger().info('动作服务端节点已启动，等待目标请求...')

    def execute_callback(self, goal_handle):
        self.get_logger().info(f'收到目标: target=({goal_handle.request.target_position.x}, '
                               f'{goal_handle.request.target_position.y}, '
                               f'{goal_handle.request.target_position.z}), speed={goal_handle.request.speed}')

        thread = threading.Thread(target=self._execute_work, args=(goal_handle,))
        thread.start()
        return

    def _execute_work(self, goal_handle):
        result = MoveRobot.Result()
        feedback = MoveRobot.Feedback()

        for i in range(10):
            if goal_handle.is_cancel_requested:
                self.get_logger().info('目标被取消')
                return
            feedback.progress = (i + 1) / 10.0
            feedback.status_message = f'移动进度: {(i+1)*10}%'
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(f'反馈进度: {feedback.progress*100:.0f}%')
            time.sleep(0.5)

        goal_handle.succeed()
        result.success = True
        result.message = '移动完成'

        self.get_logger().info('目标执行完成')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = ActionServerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('节点被 KeyboardInterrupt 终止')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()