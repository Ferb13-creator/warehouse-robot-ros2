import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import Twist


class ParamMover(Node):
    def __init__(self):
        super().__init__('param_mover')

        # 1. Declare parameters with default values
        self.declare_parameter('speed', 3.0)                  # float
        self.declare_parameter('turn_rate', 1.0)              # float
        self.declare_parameter('topic_name', '/turtle1/cmd_vel')  # string
        self.declare_parameter('enabled', True)               # bool
        self.declare_parameter('operating_mode', 'manual')

        # 2. Use a parameter value to create the publisher
        topic = self.get_parameter('topic_name').value
        self.pub = self.create_publisher(Twist, topic, 10)

        # 3. React when someone changes a parameter
        self.add_on_set_parameters_callback(self.on_param_change)

        # 4. Publish 10 times per second
        self.timer = self.create_timer(0.1, self.publish_cmd)
        self.get_logger().info('param_mover started')

    def on_param_change(self, params):
        for p in params:
            if p.name == 'speed' and not (0.0 <= p.value <= 2.0):
                return SetParametersResult(
                    successful=False, reason='speed must be between 0 and 2')
            if p.name == 'topic_name':
                self.destroy_publisher(self.pub)
                self.pub = self.create_publisher(Twist, p.value, 10)
                self.get_logger().info(f'Now publishing on {p.value}')
        return SetParametersResult(successful=True)

    def publish_cmd(self):
        if not self.get_parameter('enabled').value:
            return
        msg = Twist()
        msg.linear.x = self.get_parameter('speed').value
        msg.angular.z = self.get_parameter('turn_rate').value
        self.pub.publish(msg)


def main():
    rclpy.init()
    rclpy.spin(ParamMover())
    rclpy.shutdown()