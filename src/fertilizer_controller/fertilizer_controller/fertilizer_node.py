import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
import time

try:
    import gpiod
    hardware_available = True
except ImportError:
    hardware_available = False
    print("Warning: gpiod not available, running in simulation mode.")

RELAY_GPIO_LINE = 44

class FertilizerController(Node):
    def __init__(self):
        super().__init__('fertilizer_controller')

        if hardware_available:
            self.chip = gpiod.Chip('gpiochip0')
            self.line = self.chip.get_line(RELAY_GPIO_LINE)
            self.line.request(consumer='fertilizer', type=gpiod.LINE_REQ_DIR_OUT)
            self.line.set_value(0)  # 初始化低电平

        self.sub = self.create_subscription(Bool, '/fertilizer_trigger', self.trigger_callback, 10)

    def trigger_callback(self, msg):
        if msg.data:
            self.get_logger().info('施肥触发，打开电磁阀...')
            if hardware_available:
                self.line.set_value(1)
                time.sleep(1)
                self.line.set_value(0)
        else:
            self.get_logger().info('施肥触发信号为False，不触发动作')

    def destroy_node(self):
        if hardware_available:
            self.line.set_value(0)
            self.line.release()
            self.chip.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = FertilizerController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
