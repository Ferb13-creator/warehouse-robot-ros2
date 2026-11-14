import time
import rclpy

from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from warehouse_interfaces.action import Deliver


class DeliverServer(Node):

    def __init__(self):
        super().__init__('deliver_server')

        self.server = ActionServer(
            self,
            Deliver,
            'deliver',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info('Deliver Action Server Ready')

    # Reject invalid goals
    def goal_callback(self, goal_request):

        if (not goal_request.destination.strip()
                or goal_request.distance <= 0.0
                or goal_request.speed <= 0.0):

            self.get_logger().warn('Invalid delivery goal')
            return GoalResponse.REJECT

        self.get_logger().info('Delivery goal accepted')
        return GoalResponse.ACCEPT

    # Allow cancellation
    def cancel_callback(self, goal_handle):

        self.get_logger().info('Cancel requested')

        return CancelResponse.ACCEPT

    # Execute delivery
    def execute_callback(self, goal_handle):

        goal = goal_handle.request

        distance = goal.distance
        speed = goal.speed

        travelled = 0.0
        start_time = time.monotonic()

        feedback = Deliver.Feedback()
        result = Deliver.Result()

        self.get_logger().info(
            f'Delivering to {goal.destination}'
        )

        step = 0.5

        while travelled < distance:

            # Check cancellation
            if goal_handle.is_cancel_requested:

                goal_handle.canceled()

                result.success = False
                result.time_taken = time.monotonic() - start_time

                self.get_logger().info('Delivery cancelled')

                return result

            # Calculate travelled distance
            travelled = min(
                travelled + speed * step,
                distance
            )

            # Calculate feedback
            feedback.remaining_distance = distance - travelled

            feedback.percent = (travelled / distance) * 100.0

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f'Remaining: {feedback.remaining_distance:.2f} m, '
                f'Progress: {feedback.percent:.1f}%'
            )

            time.sleep(step)

        # Delivery completed
        goal_handle.succeed()

        result.success = True
        result.time_taken = time.monotonic() - start_time

        self.get_logger().info('Delivery completed')

        return result


def main(args=None):

    rclpy.init(args=args)

    node = DeliverServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()

    except KeyboardInterrupt:
        pass

    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
