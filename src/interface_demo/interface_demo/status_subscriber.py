import rclpy
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus


class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('status_subscriber')
        self.create_subscription(RobotStatus, 'robot_status', self.callback, 10)

    def callback(self, msg):
        mode = 'AUTO' if msg.mode == RobotStatus.MODE_AUTO else 'MANUAL'
        self.get_logger().info(
            f'{msg.robot_name}: battery={msg.battery:.0f}% '
            f'temp={msg.temperature:.1f}C moving={msg.is_moving} mode={mode}')


def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()