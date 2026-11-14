import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class RobotClient(Node):

    def __init__(self):
        super().__init__('robot_client')

        self.client = self.create_client(
            SetBool,
            'robot_control'
        )

    def send_request(self, value):

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')

        request = SetBool.Request()
        request.data = value

        future = self.client.call_async(request)

        future.add_done_callback(self.response_callback)

    def response_callback(self, future):

        response = future.result()

        self.get_logger().info(
            f'Success: {response.success}'
        )

        self.get_logger().info(
            f'Message: {response.message}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = RobotClient()

    node.send_request(False)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()