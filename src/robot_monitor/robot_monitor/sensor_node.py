
import random
import rclpy

from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger


class SensorNode(Node):

    def __init__(self):
        super().__init__('sensor_node')

        # Parameters
        self.declare_parameter('robot_name', 'robot1')
        self.declare_parameter('publish_rate', 1.0)
        self.declare_parameter('drain_rate', 2.0)
        self.declare_parameter('start_battery', 100.0)

        rate = self.get_parameter('publish_rate').value
        self.battery = self.get_parameter('start_battery').value
        self.temperature = 30.0
        self.period = 1.0 / rate

        # Publishers
        self.battery_pub = self.create_publisher(
            Float32, 'battery_level', 10)

        self.temp_pub = self.create_publisher(
            Float32, 'temperature', 10)

        # New motor current publisher
        self.motor_current_pub = self.create_publisher(
            Float32, 'motor_current', 10)

        # Service server
        self.create_service(
            Trigger, 'reset_battery', self.reset_callback)

        self.create_timer(self.period, self.timer_callback)

        self.get_logger().info('Sensor node started')

    def timer_callback(self):

        drain = self.get_parameter('drain_rate').value

        self.battery = max(
            0.0, self.battery - drain * self.period)

        self.temperature = (
            30.0 + 5.0 * drain + random.uniform(-2.0, 2.0)
        )

        # Motor current increases with drain rate
        current = 2.0 + (0.5 * drain) + random.uniform(-0.2, 0.2)

        # Battery message
        b = Float32()
        b.data = float(self.battery)
        self.battery_pub.publish(b)

        # Temperature message
        t = Float32()
        t.data = float(self.temperature)
        self.temp_pub.publish(t)

        # Motor current message
        c = Float32()
        c.data = float(current)
        self.motor_current_pub.publish(c)

    def reset_callback(self, request, response):

        self.battery = 100.0

        response.success = True
        response.message = 'Battery reset to 100%'

        self.get_logger().info('Battery recharged')

        return response


def main(args=None):

    rclpy.init(args=args)
    node = SensorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
