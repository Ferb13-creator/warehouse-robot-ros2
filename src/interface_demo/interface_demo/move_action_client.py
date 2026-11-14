import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from robot_interfaces.action import RobotMove


class MoveActionClient(Node):
    def __init__(self):
        super().__init__('move_action_client')
        self._client = ActionClient(self, RobotMove, 'robot_move')

    def send_goal(self, distance, speed):
        self.get_logger().info('Waiting for action server...')
        self._client.wait_for_server()

        goal = RobotMove.Goal()
        goal.target_distance = distance
        goal.speed = speed

        future = self._client.send_goal_async(
            goal, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return
        self.get_logger().info('Goal accepted')
        goal_handle.get_result_async().add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'Progress: {fb.progress_percent:.0f}% ({fb.current_distance:.1f} m)')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f'Result: success={result.success}, '
            f'travelled={result.distance_travelled:.1f} m, '
            f'message="{result.message}"')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    distance = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    speed = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    node = MoveActionClient()
    node.send_goal(distance, speed)
    rclpy.spin(node)