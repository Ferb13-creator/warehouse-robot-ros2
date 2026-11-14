
import rclpy

from rclpy.node import Node
from std_msgs.msg import Float32, String
from std_srvs.srv import Trigger, SetBool


class MonitorNode(Node):

    def __init__(self):
        super().__init__('monitor_node')

        # Parameters
        self.declare_parameter('battery_warn', 30.0)
        self.declare_parameter('battery_critical', 10.0)
        self.declare_parameter('temp_limit', 60.0)
        self.declare_parameter('current_limit', 5.0)
        self.declare_parameter('auto_recharge', False)

        # Latest sensor readings
        self.battery = 100.0
        self.temperature = 0.0
        self.motor_current = 0.0

        self.recharge_pending = False

        # Monitoring enabled by default
        self.monitoring_enabled = True

        # Subscribers
        self.create_subscription(
            Float32,
            'battery_level',
            self.battery_callback,
            10
        )

        self.create_subscription(
            Float32,
            'temperature',
            self.temp_callback,
            10
        )

        # New motor current subscriber
        self.create_subscription(
            Float32,
            'motor_current',
            self.current_callback,
            10
        )

        # Status publisher
        self.status_pub = self.create_publisher(
            String, 'robot_status', 10)

        # Existing service client
        self.reset_client = self.create_client(
            Trigger, 'reset_battery')

        # New monitoring service
        self.create_service(
            SetBool,
            'set_monitoring',
            self.monitoring_callback
        )

        # Evaluate status every second
        self.create_timer(1.0, self.evaluate_status)

        self.get_logger().info('Monitor node started')

    def battery_callback(self, msg):

        self.battery = msg.data

        critical = self.get_parameter(
            'battery_critical').value

        auto = self.get_parameter(
            'auto_recharge').value

        if (
            self.battery <= critical
            and auto
            and not self.recharge_pending
        ):
            self.get_logger().warn(
                'Battery critical, requesting recharge')

            self.request_recharge()

    def temp_callback(self, msg):
        self.temperature = msg.data

    # New current callback
    def current_callback(self, msg):
        self.motor_current = msg.data

    # New monitoring service callback
    def monitoring_callback(self, request, response):

        self.monitoring_enabled = request.data

        if request.data:
            response.success = True
            response.message = 'Monitoring enabled. Status publishing resumed.'

            self.get_logger().info(response.message)

        else:
            response.success = True
            response.message = 'Monitoring disabled. Status publishing stopped.'

            self.get_logger().info(response.message)

        return response

    def request_recharge(self):

        if not self.reset_client.service_is_ready():

            self.get_logger().warn(
                'reset_battery service is not available')

            return

        self.recharge_pending = True

        future = self.reset_client.call_async(
            Trigger.Request())

        future.add_done_callback(self.recharge_done)

    def recharge_done(self, future):

        self.recharge_pending = False

        try:
            result = future.result()
            self.get_logger().info(
                f'Recharge result: {result.message}')

        except Exception as e:
            self.get_logger().error(
                f'Recharge failed: {e}')

    def evaluate_status(self):

        # Stop status publishing when monitoring is disabled
        if not self.monitoring_enabled:
            return

        warn = self.get_parameter(
            'battery_warn').value

        limit = self.get_parameter(
            'temp_limit').value

        current_limit = self.get_parameter(
            'current_limit').value

        problems = []

        if self.battery < warn:
            problems.append('LOW BATTERY')

        if self.temperature > limit:
            problems.append('HIGH TEMPERATURE')

        # New high-current check
        if self.motor_current > current_limit:
            problems.append('HIGH CURRENT')

        if problems:

            text = 'WARNING: ' + ', '.join(problems)

            self.get_logger().warn(text)

        else:
            text = 'OK'

        msg = String()

        msg.data = (
            f'{text} | '
            f'battery={self.battery:.1f}% '
            f'temp={self.temperature:.1f}C '
            f'current={self.motor_current:.2f}A'
        )

        self.status_pub.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = MonitorNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
