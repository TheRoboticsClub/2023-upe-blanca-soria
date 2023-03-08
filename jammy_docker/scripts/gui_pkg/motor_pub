import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CMDVel ():
    def __init__(self):

        self.vx = 0 # vel in x[m/s] (use this for V in wheeled robots)
        self.vy = 0 # vel in y[m/s]
        self.vz = 0 # vel in z[m/s]
        self.ax = 0 # angular vel in X axis [rad/s]
        self.ay = 0 # angular vel in X axis [rad/s]
        self.az = 0 # angular vel in Z axis [rad/s] (use this for W in wheeled robots)
        self.timeStamp = 0 # Time stamp [s]

    def __str__(self):
        s = "CMDVel: {\n   vx: " + str(self.vx) + "\n   vy: " + str(self.vy)
        s = s + "\n   vz: " + str(self.vz) + "\n   ax: " + str(self.ax) 
        s = s + "\n   ay: " + str(self.ay) + "\n   az: " + str(self.az)
        s = s + "\n   timeStamp: " + str(self.timeStamp)  + "\n}"
        return s 
    
def cmdvel2Twist(vel):
    tw = Twist()
    tw.linear.x = float(vel.vx)
    tw.linear.y = float(vel.vy)
    tw.linear.z = float(vel.vz)
    tw.angular.x = float(vel.ax)
    tw.angular.y = float(vel.ay)
    tw.angular.z = float(vel.az)
    return tw
    
class MotorPublisher(Node):
    def __init__(self):
        super().__init__('motor_publisher')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10 ) 
        self.cmdvel = CMDVel()
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.inc = 0.05

    def publish(self):
        tw = cmdvel2Twist(self.cmdvel)
        self.pub.publish(tw)

    def timer_callback(self):
        self.cmdvel.vx = 0.2
        self.cmdvel.vy = self.cmdvel.vy + self.inc
        self.publish()

def main(args=None):
    rclpy.init(args=args)
    motor_pub = MotorPublisher()
    rclpy.spin(motor_pub)
    motor_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
