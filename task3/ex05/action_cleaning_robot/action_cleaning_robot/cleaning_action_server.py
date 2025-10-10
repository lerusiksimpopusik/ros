import rclpy
import math
import sys
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from cleaning_action_interfaces.action import CleaningTask


class CleaningActionServer(Node):
    def __init__(self):
        super().__init__('cleaning_action_server')

        self._action_server = ActionServer(
            self,
            CleaningTask,
            'cleaning_task',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        self.pose = None

    def goal_callback(self, goal_request):
        self.get_logger().info(f'Received goal request: {goal_request.task_type}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_request):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def pose_callback(self, msg):
        self.pose = msg

    def execute_callback(self, goal_request):
        self.get_logger().info(f'Executing task: {goal_request.request.task_type}')
        self.goal_request = goal_request

        feedback_msg = CleaningTask.Feedback()
        self.cleaned_points = 0
        self.distance_travelled = 0.0

        start_x = self.pose.x if self.pose else 5.5
        start_y = self.pose.y if self.pose else 5.5

        goal = goal_request.request

        if goal.task_type == "clean_square":
            size = goal.area_size
            robot_size = 0.5
            n_parts = int(size / robot_size)
            part_width = size / n_parts
            self._turn_to_angle(0)
            
            for strip in range(n_parts+1):
                self._move_to_point(start_x + size * (strip % 2 == 0), self.pose.y)
                self.distance_travelled += size
                self.cleaned_points += 1
                
                if strip < n_parts:
                    self._turn_to_angle(-math.pi/2)
                    self._move_to_point(self.pose.x, self.pose.y - part_width)
                    self.cleaned_points += 1
                    self.distance_travelled += part_width
                    if strip % 2 == 0:
                        self._turn_to_angle(math.pi)
                    else:
                        self._turn_to_angle(0)
                feedback_msg.current_cleaned_points = self.cleaned_points
                feedback_msg.progress_percent = int((strip + 1) / (n_parts+1) * 100)
                feedback_msg.current_x = self.pose.x
                feedback_msg.current_y = self.pose.y
                self.goal_request.publish_feedback(feedback_msg)

        elif goal.task_type == "return_home":
            target_x, target_y = self.goal_request.request.target_x, self.goal_request.request.target_y

            dx = target_x - start_x
            dy = target_y - start_y
            initial_distance = math.sqrt(dx * dx + dy * dy)

            curr_dx = target_x - self.pose.x
            curr_dy = target_y - self.pose.y
            current_dist = math.sqrt(curr_dx * curr_dx + curr_dy * curr_dy)
            self._move_to_point(target_x, target_y)
        
            feedback_msg.progress_percent = max(0, min(100, int(100 - current_dist * 10)))
            feedback_msg.current_x = self.pose.x
            feedback_msg.current_y = self.pose.y
            self.goal_request.publish_feedback(feedback_msg)
            self.distance_travelled = initial_distance

        goal_request.succeed()

        result = CleaningTask.Result()
        result.success = True
        result.cleaned_points = self.cleaned_points
        result.total_distance = self.distance_travelled
        return result

    def _move_to_point(self, target_x, target_y):
        while True:
            if self.goal_request.is_cancel_requested:
                self.get_logger().info('Task canceled')
                result = CleaningTask.Result()
                result.cleaned_points = self.cleaned_points
                result.total_distance = self.distance_travelled
                result.success = False
                result.message = "Task canceled"
                return result
            dx = target_x - self.pose.x
            dy = target_y - self.pose.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 0.05:
                break
            angle_diff = math.atan2(dy, dx) - self.pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
            twist = Twist()
            if abs(angle_diff) > 0.1:
                twist.angular.z = 2.0 * angle_diff
            else:
                twist.angular.z = 0.0
                twist.linear.x = 2.0
            self.cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.05)

    def _turn_to_angle(self, target_theta):
        target_theta = math.atan2(math.sin(target_theta), math.cos(target_theta))
        while True:
            twist = Twist()
            angle_diff = target_theta - self.pose.theta
            angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
            if angle_diff < 0.05:
                break
            twist.angular.z = angle_diff
            self.cmd_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.05)


def main(args=None):
    rclpy.init(args=args)
    node = CleaningActionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except ExternalShutdownException:
        sys.exit(1)
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
