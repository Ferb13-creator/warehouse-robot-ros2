import sys

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class Client(Node):

    def __init__(self):
        super().__init__('calculator_client')

        self.client = self.create_client(
            AddTwoInts,
            'add_two_ints'
        )

    def send_request(self, a, b):

        # Wait for the server
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for server...')

        # Create a request
        request = AddTwoInts.Request()

        # Send two variables
        request.a = a
        request.b = b

        # Send the request
        return self.client.call_async(request)


def main(args=None):

    rclpy.init(args=args)

    # Check command-line arguments
    if len(sys.argv) != 3:
        print('Usage: ros2 run telemetry_core clientt <a> <b>')
        rclpy.shutdown()
        return

    # Convert arguments to integers
    try:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    except ValueError:
        print('Error: Enter two integers.')
        rclpy.shutdown()
        return

    node = Client()

    try:
        # Send a and b to the server
        future = node.send_request(a, b)

        # Wait for the response
        rclpy.spin_until_future_complete(node, future)

        response = future.result()

        if response is not None:
            node.get_logger().info(f'a = {a}')
            node.get_logger().info(f'b = {b}')
            node.get_logger().info(
                f'Sum received from server = {response.sum}'
            )
        else:
            node.get_logger().error('Service call failed')

    except Exception as e:
        node.get_logger().error(f'Error: {e}')

    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()