
import math
import time

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class GlobalVelocityNode(Node):
    def __init__(self):
        super().__init__('global_velocity_node')

        self.last_print_time = 0.0

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info('Node global velocity aktif.')
        self.get_logger().info('Menunggu data dari /odom...')

    def odom_callback(self, msg):
        q = msg.pose.pose.orientation

        yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

        vx_local = msg.twist.twist.linear.x
        vy_local = msg.twist.twist.linear.y
        omega = msg.twist.twist.angular.z

        vx_global = (
            vx_local * math.cos(yaw)
            - vy_local * math.sin(yaw)
        )

        vy_global = (
            vx_local * math.sin(yaw)
            + vy_local * math.cos(yaw)
        )

        current_time = time.monotonic()

        if current_time - self.last_print_time >= 0.5:
            self.get_logger().info(
                f'Vx Global: {vx_global:.3f} m/s | '
                f'Vy Global: {vy_global:.3f} m/s | '
                f'Yaw: {math.degrees(yaw):.2f} deg | '
                f'Angular Z: {omega:.3f} rad/s'
            )

            self.last_print_time = current_time


def main(args=None):
    rclpy.init(args=args)
    node = GlobalVelocityNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
