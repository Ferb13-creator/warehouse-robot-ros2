import time
import rclpy
from rclpy.action import ActionServer, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from robot_interfaces.action import RobotMove


class MoveActionServer(Node):
    def __init__(self):
        super().__init__('move_action_server')
        self._server = ActionServer(
            self, RobotMove, 'robot_move',
            execute_callback=self.execute_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup())
        self.get_logger().info('RobotMove action server ready')

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Cancel requested')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        target = goal_handle.request.target_distance
        speed = goal_handle.request.speed
        result = RobotMove.Result()

        # Reject nonsense goals
        if target <= 0.0 or speed <= 0.0:
            self.get_logger().warn('Invalid goal: distance and speed must be > 0')
            goal_handle.abort()
            result.success = False
            result.message = 'Invalid goal'
            return result

        self.get_logger().info(f'Moving {target:.1f} m at {speed:.1f} m/s')
        feedback = RobotMove.Feedback()
        distance = 0.0
        step = 0.5   # seconds per update

        while distance < target:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.distance_travelled = distance
                result.message = 'Cancelled'
                return result

            distance = min(distance + speed * step, target)
            feedback.current_distance = distance
            feedback.progress_percent = distance / target * 100.0
            goal_handle.publish_feedback(feedback)
            time.sleep(step)

        goal_handle.succeed()
        result.success = True
        result.distance_travelled = distance
        result.message = 'Target reached'
        return result


def main(args=None):
    rclpy.init(args=args)
    node = MoveActionServer()
    executor = MultiThreadedExecutor()
    try:
        rclpy.spin(node, executor=executor)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()