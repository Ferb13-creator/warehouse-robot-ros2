import rclpy
from rclpy.node import Node
from robot_interfaces.srv import SetSpeed


class SpeedServer(Node):
    def __init__(self):
        super().__init__('speed_server')
        self.speed = 0.0
        self.create_service(SetSpeed, 'set_speed', self.callback)
        self.get_logger().info('Speed service ready')

    def callback(self, request, response):
        response.previous_speed = self.speed
        if request.speed < 0.0 or request.speed > 2.0:
            response.success = False
            response.message = 'Speed must be between 0.0 and 2.0'
        else:
            self.speed = request.speed
            response.success = True
            response.message = f'Speed set to {self.speed:.2f}'
        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = SpeedServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()