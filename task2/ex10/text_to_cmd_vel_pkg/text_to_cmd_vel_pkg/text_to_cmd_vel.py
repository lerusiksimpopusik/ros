# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TextToCmdVel(Node):
    def __init__(self):
        super().__init__('text_to_cmd_vel')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            String,
            '/cmd_text',
            self.text_callback,
            10
        )
        self.get_logger().info('TextToCmdVel node started, listening to /cmd_text')

    def text_callback(self, msg):
        twist = Twist()
        command = msg.data.lower()

        if command == 'move_forward':
            twist.linear.x = 1.0
            self.get_logger().info('Moving forward: linear.x = 1.0')
        elif command == 'move_backward':
            twist.linear.x = -1.0
            self.get_logger().info('Moving backward: linear.x = -1.0')
        elif command == 'turn_left':
            twist.angular.z = 1.5
            self.get_logger().info('Turning left: angular.z = 1.5')
        elif command == 'turn_right':
            twist.angular.z = -1.5
            self.get_logger().info('Turning right: angular.z = -1.5')
        else:
            self.get_logger().warn(f'Unknown command: {command}')
            return

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TextToCmdVel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
