import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool


class RobotService(Node):

    def __init__(self):
        super().__init__('robot_service')

        self.service = self.create_service(
            SetBool,
            'robot_control',
            self.control_robot
        )

        self.get_logger().info('Robot service is ready')

    def control_robot(self, request, response):

        if request.data:
            response.success = True
            response.message = 'Robot stopped'
        else:
            response.success = True
            response.message = 'Robot started'

        return response


def main(args=None):
    rclpy.init(args=args)

    node = RobotService()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()