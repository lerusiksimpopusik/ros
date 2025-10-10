import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import sys
import math

class MoveToGoal(Node):
    def __init__(self, goal_x, goal_y, goal_theta):
        super().__init__('move_to_goal')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pose = None

        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_theta = goal_theta

        self.state = "move"
        self.timer = self.create_timer(0.1, self.control_loop)

    def pose_callback(self, msg):
        self.pose = msg

    def control_loop(self):
        if self.pose is None:
            return

        twist = Twist()

        if self.state == "move":
            dx = self.goal_x - self.pose.x
            dy = self.goal_y - self.pose.y
            distance = math.sqrt(dx**2 + dy**2)

            angle_diff = math.atan2(dy, dx) - self.pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

            if distance > 0.1:
                if abs(angle_diff) > 0.1:
                    twist.angular.z = 2.0 * angle_diff
                    twist.linear.x = 0.0
                else:
                    twist.linear.x = 2.0
                    twist.angular.z = 0.0
            else:
                self.get_logger().info("Point reached, start rotation.")
                self.state = "rotate"
                self.get_logger().info(f"state = {self.state}")

        elif self.state == "rotate":
            angle_diff = self.goal_theta - self.pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

            if abs(angle_diff) > 0.05:
                twist.angular.z = 2.0 * angle_diff
            else:
                self.get_logger().info("Goal reached")
                twist = Twist()
                self.state = "done"
                self.get_logger().info(f"state = {self.state}")
                return

        self.pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 4:
        print("Usage: ros2 run move_to_goal move_to_goal x y theta")
        return

    node = MoveToGoal(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))

    while rclpy.ok() and not node.state == "done":
        rclpy.spin_once(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
