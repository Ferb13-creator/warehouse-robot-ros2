import sys
import rclpy
from rclpy.node import Node
from robot_interfaces.srv import SetSpeed


def main(args=None):
    rclpy.init(args=args)
    node = Node('speed_client')
    client = node.create_client(SetSpeed, 'set_speed')

    speed = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0

    if not client.wait_for_service(timeout_sec=3.0):
        node.get_logger().error('Service set_speed not available')
        node.destroy_node()
        rclpy.try_shutdown()
        return

    request = SetSpeed.Request()
    request.speed = speed
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    result = future.result()
    node.get_logger().info(
        f'success={result.success}, message="{result.message}", '
        f'previous_speed={result.previous_speed:.2f}')

    node.destroy_node()
    rclpy.try_shutdown()