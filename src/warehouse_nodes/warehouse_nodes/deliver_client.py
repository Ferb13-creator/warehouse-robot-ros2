import sys
import rclpy

from rclpy.node import Node
from rclpy.action import ActionClient

from warehouse_interfaces.action import Deliver


class DeliverClient(Node):

    def __init__(self):
        super().__init__('deliver_client')

        self.client = ActionClient(
            self,
            Deliver,
            'deliver'
        )

        self.goal_handle = None

    def send_goal(self, destination, distance, speed):

        self.get_logger().info('Waiting for action server...')

        self.client.wait_for_server()

        goal = Deliver.Goal()

        goal.destination = destination
        goal.distance = distance
        goal.speed = speed

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):

        self.goal_handle = future.result()

        if not self.goal_handle.accepted:

            self.get_logger().info('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')

        result_future = self.goal_handle.get_result_async()

        result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Remaining distance: '
            f'{feedback.remaining_distance:.2f} m, '
            f'Progress: {feedback.percent:.1f}%'
        )

    def cancel_goal(self):

        if self.goal_handle is not None:

            self.get_logger().info('Sending cancel request')

            return self.goal_handle.cancel_goal_async()

        return None

    def result_callback(self, future):

        result = future.result().result

        self.get_logger().info(
            f'Success: {result.success}, '
            f'Time taken: {result.time_taken:.2f} seconds'
        )

        rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    destination = sys.argv[1] if len(sys.argv) > 1 else 'Warehouse_B'
    distance = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

    node = DeliverClient()

    try:
        node.send_goal(destination, distance, speed)
        rclpy.spin(node)

    except KeyboardInterrupt:
        if node.goal_handle is not None and rclpy.ok():

            future = node.cancel_goal()

            if future is not None:
                rclpy.spin_until_future_complete(node, future)

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
