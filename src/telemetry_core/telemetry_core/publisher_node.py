import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')

        self.publisher = self.create_publisher(
            String,
            'robot_status',
            10
        )

        self.battery = 100

        self.timer = self.create_timer(
            1.0,
            self.publish_message
        )

    def publish_message(self):
        msg = String()

        if self.battery > 20:
            msg.data = f'battery percentage is healthy {self.battery}'
            self.publisher.publish(msg)
            self.get_logger().info(f'Publishing: {msg.data}')
            self.battery -= 1

        elif self.battery > 0:
            msg.data = f'battery percentage is low {self.battery}'
            self.publisher.publish(msg)
            self.get_logger().info(f'Publishing: {msg.data}')
            self.battery -= 1

        else:
            msg.data = f'your battery is dead {self.battery}'
            self.publisher.publish(msg)
            self.get_logger().info(f'Publishing: {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    node = PublisherNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

