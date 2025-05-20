import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import torch
import cv2
import numpy as np

class CropDetectorNode(Node):
    def __init__(self):
        super().__init__('crop_detector_node')
        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()

        self.get_logger().info('加载YOLOv5模型...')
        self.detector = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.get_logger().info('模型加载完成，等待图像...')

    def image_callback(self, msg):
        # 将ROS图像消息转换为OpenCV格式
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # 推理
        results = self.detector(cv_image)

        # 解析检测结果
        for *box, conf, cls in results.xyxy[0]:
            label = self.detector.names[int(cls)]
            if label == 'crop':
                self.get_logger().info('识别到作物行')
            elif label == 'canal':
                self.get_logger().info('识别到水渠')

def main(args=None):
    rclpy.init(args=args)
    node = CropDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
