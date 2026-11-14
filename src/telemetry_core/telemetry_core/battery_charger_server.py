import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci


class BatteryChargerServer(Node):

    def __init__(self):
        super().__init__('dock_and_charge')

        self.action_server = ActionServer(
            self,
            Fibonacci,
            'dock_and_charge',
            self.execute_callback
        )

        self.get_logger().info('Charging started...')

    def execute_callback(self, goal_handle):
        order = goal_handle.request.order

        self.get_logger().info(f'Current Battery Stage: {order}')

        sequence = [0, 20]
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

        self.get_logger().info('Charging Completed!')

        return result


def main(args=None):
    rclpy.init(args=args)
    node = BatteryChargerServer()

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