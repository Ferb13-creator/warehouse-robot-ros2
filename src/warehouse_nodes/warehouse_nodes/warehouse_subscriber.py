import rclpy
from rclpy.node import Node

from warehouse_interfaces.msg import DeliveryStatus


class WarehouseSubscriber(Node):

    def __init__(self):
        super().__init__('warehouse_subscriber')

        self.subscription = self.create_subscription(
            DeliveryStatus,
            'delivery_status',
            self.status_callback,
            10
        )

        self.get_logger().info('Warehouse Subscriber Started')

    def status_callback(self, msg):
        self.get_logger().info(
            f'Received Status: Robot={msg.robot_id}, '
            f'Packages={msg.package_count}, '
            f'Battery={msg.battery}%, '
            f'State={msg.state}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = WarehouseSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
