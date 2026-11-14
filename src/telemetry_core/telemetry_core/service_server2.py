import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class Server(Node):

    def __init__(self):
        super().__init__('calculator_server')

        self.service = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints
        )

        self.get_logger().info('Server is ready')

    def add_two_ints(self, request, response):

        response.sum = request.a + request.b

        self.get_logger().info(
            f'{request.a} + {request.b} = {response.sum}'
        )

        return response


def main():
    rclpy.init()

    node = Server()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()