import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci


class StudentActionClient(Node):

    def __init__(self):
        super().__init__('dock_and_charge')

        self.action_client = ActionClient(
            self,
            Fibonacci,
            'dock_and_charge'
        )

    def send_goal(self, order):
        self.action_client.wait_for_server()

        goal = Fibonacci.Goal()
        goal.order = order

        self.get_logger().info(f'Charging started...: {order}')

        future = self.action_client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Charging completed!')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback.partial_sequence
        self.get_logger().info(f'Feedback: {feedback}')

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Final result: {result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = StudentActionClient()

    try:
        node.send_goal(5)
        rclpy.spin(node)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()