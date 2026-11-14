import rclpy
from rclpy.node import Node

from warehouse_interfaces.msg import DeliveryStatus
from warehouse_interfaces.srv import LoadPackage


class WarehousePublisher(Node):

    def __init__(self):
        super().__init__('warehouse_publisher')

        self.package_count = 0
        self.battery = 100.0

        self.publisher = self.create_publisher(
            DeliveryStatus, 'delivery_status', 10
        )

        self.service = self.create_service(
            LoadPackage, 'load_package', self.load_package_callback
        )

        self.timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Warehouse Publisher Started')

    def publish_status(self):
        msg = DeliveryStatus()
        msg.robot_id = 'Robot_01'
        msg.package_count = self.package_count
        msg.battery = self.battery
        msg.state = DeliveryStatus.STATE_IDLE

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Published: Packages={msg.package_count}, '
            f'Battery={msg.battery}%'
        )

    def load_package_callback(self, request, response):

        if request.weight <= 0:
            response.accepted = False
            response.message = 'Invalid package weight'
        elif request.weight > 10.0:
            response.accepted = False
            response.message = 'Package exceeds 10 kg limit'
        elif self.package_count >= 5:
            response.accepted = False
            response.message = 'Warehouse robot is full'
        else:
            self.package_count += 1
            response.accepted = True
            response.message = f'Package {request.package_id} loaded'

        response.total_packages = self.package_count

        self.get_logger().info(response.message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = WarehousePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
