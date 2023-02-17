import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class ImageSub(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(Image,'/depth_camera/image_raw',self.img_callback,10)
        self.subscription  # prevent unused variable warning

    def img_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        try:
            # Convert your ROS2 Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError:
            print(error)
        else:
            winname = "Turtlebot2 camera"
            cv2.namedWindow(winname)        # Create a named window
            cv2.moveWindow(winname, 0,0)
            cv2.imshow(winname,cv2_img)
            cv2.waitKey(2)


def main(args=None):
    rclpy.init(args=args)
    img_sub = ImageSub()
    rclpy.spin(img_sub)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    img_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()