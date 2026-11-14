import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class GPSPublisher(Node):

    def __init__(self):
        super().__init__('gps_publisher')

        self.publisher = self.create_publisher(
            String,
            'gps_data',
            10
        )

        self.timer = self.create_timer(
            2.0,
            self.publish_gps
        )

        self.latitude = 10.8505
        self.longitude = 76.2711

    def publish_gps(self):
        msg = String()


        formatted_data = (

            f"\n============GPS DATA=========== \n"
            f"Robot id: {self.robot_id}\n"
            f"speed : {self.speed}m/s \n"
            f"latitude: {self.latitude}\n"
            f"longitude: {self.longitude}\n"

        )
        msg=formatted_data
        msg.data = f'Latitude: {self.latitude}, Longitude:{self.longitude}'

        self.publisher.publish(msg)

        self.get_logger().info(f'Publishing: {msg.data}')


def main(args=None):
    rclpy.init(args=args)

    node = GPSPublisher()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()