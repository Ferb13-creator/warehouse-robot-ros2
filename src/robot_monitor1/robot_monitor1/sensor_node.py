import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        # Parameter: how many % the battery loses per second
        self.declare_parameter('drain_rate', 0.5)

        self.battery = 100.0
        self.battery_pub = self.create_publisher(Float32, '/battery_level', 10)
        self.temp_pub = self.create_publisher(Float32, '/temperature', 10)
        self.timer = self.create_timer(1.0, self.update)   # runs once per second
        self.get_logger().info('Sensor node started')

    def update(self):
        # Read the parameter every tick so "ros2 param set" works live
        rate = self.get_parameter('drain_rate').value
        self.battery = max(0.0, self.battery - rate)

        # Temperature rises as the battery drains
        temperature = 25.0 + (100.0 - self.battery) * 0.5

        b = Float32()
        b.data = self.battery
        t = Float32()
        t.data = temperature
        self.battery_pub.publish(b)
        self.temp_pub.publish(t)
        self.get_logger().info(f'battery={self.battery:.1f}  temp={temperature:.1f}')


def main():
    rclpy.init()
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()