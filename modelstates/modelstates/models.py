import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import GetEntityState
import time

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.client = self.create_client(GetEntityState, '/demo/get_entity_state')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = GetEntityState.Request()

    def get_model_state(self, model_name):
        self.req.name = model_name
        future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            return future.result()
        else:
            return None

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    model_state = node.get_model_state('roombaROS')
    if model_state is not None:
        node.get_logger().info('Model position: {}'.format(model_state.state.pose.position))
        node.get_logger().info('Model orientation: {}'.format(model_state.state.pose.orientation))
    else:
        node.get_logger().warn('Failed to get model state')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()