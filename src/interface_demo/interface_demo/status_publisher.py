import rclpy
from rclpy.node import Node
from robot_interfaces.msg import RobotStatus


class StatusPublisher(Node):
    def __init__(self):
        super().__init__('status_publisher')
        self.pub = self.create_publisher(RobotStatus, 'robot_status', 10)
        self.battery = 100.0
        self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Status publisher started')

    def timer_callback(self):
        self.battery = max(0.0, self.battery - 1.0)

        msg = RobotStatus()
        msg.robot_name = 'robot1'
        msg.battery = self.battery
        msg.temperature = 35.0
        msg.is_moving = True
        msg.mode = RobotStatus.MODE_AUTO   # use the constant

        self.pub.publish(msg)
        self.get_logger().info(f'Published battery {msg.battery:.0f}%')


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()