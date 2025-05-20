import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
import time

class MasterController(Node):
    def __init__(self):
        super().__init__('master_controller')
        self.subscription = self.create_subscription(
            String,
            '/crop_detector/info',
            self.info_callback,
            10
        )
        self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.fertilizer_publisher = self.create_publisher(Bool, '/fertilizer_trigger', 10)

        self.last_fertilize_time = self.get_clock().now().seconds_nanoseconds()[0]

    def info_callback(self, msg):
        info = msg.data
        cmd = Twist()

        if info == 'crop':
            self.get_logger().info('识别到作物行，直行中...')
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
        elif info == 'canal':
            self.get_logger().info('识别到水渠，停止...')
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_publisher.publish(cmd)

        now = self.get_clock().now().seconds_nanoseconds()[0]
        if now - self.last_fertilize_time > 10:
            self.get_logger().info('触发施肥动作：发布电磁阀信号')
            fert_msg = Bool()
            fert_msg.data = True
            self.fertilizer_publisher.publish(fert_msg)
            self.last_fertilize_time = now

def main(args=None):
    rclpy.init(args=args)
    node = MasterController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
