import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci


class StudentActionServer(Node):

    def __init__(self):
        super().__init__('student_action_server')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'student_fibonacci',
            self.execute_callback
        )

        self.get_logger().info('Action server is ready')

    def execute_callback(self, goal_handle):
        order = goal_handle.request.order

        self.get_logger().info(f'Goal received: {order}')

        sequence = [0, 1]
        feedback = Fibonacci.Feedback()
        feedback.partial_sequence = sequence

        for i in range(1, order):
            sequence.append(sequence[i] + sequence[i - 1])

            feedback.partial_sequence = sequence.copy()
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f'Feedback: {feedback.partial_sequence}'
            )

            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = sequence

        self.get_logger().info('Goal completed')

        return result


def main(args=None):
    rclpy.init(args=args)
    node = StudentActionServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()