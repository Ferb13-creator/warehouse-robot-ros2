import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SimpleSquare(Node):

    def __init__(self):
        super().__init__('simple_square')

        self.pub = self.create_publisher(
            Twist, '/turtle1/cmd_vel', 10)

        self.side = 0
        self.turning = False
        self.start_time = self.get_clock().now()

        self.speed = 2.0
        self.turn_rate = 1.57
        self.move_time = 2.0
        self.turn_time = 1.0

        self.timer = self.create_timer(0.01, self.move_square)

    def move_square(self):
        msg = Twist()

        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        if not self.turning:
            if elapsed < self.move_time:
                msg.linear.x = self.speed
            else:
                self.turning = True
                self.start_time = self.get_clock().now()

        else:
            if elapsed < self.turn_time:
                msg.angular.z = self.turn_rate
            else:
                self.side += 1
                self.side %= 4
                self.turning = False
                self.start_time = self.get_clock().now()

        self.pub.publish(msg)


def main():
    rclpy.init()
    node = SimpleSquare()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()