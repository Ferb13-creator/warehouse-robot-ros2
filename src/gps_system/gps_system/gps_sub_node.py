import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GPSSubscriber(Node):

    def __init__(self):
        super().__init__('gps_subscriber')

        self.subscription = self.create_subscription(
            String,
            'gps_data',
            self.gps_callback,
            10
        )

    def gps_callback(self, msg):
            self.get_logger().info(f'GPS Received: {msg.data}')        



def main(args=None):
    rclpy.init(args=args)

    node = GPSSubscriber()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()