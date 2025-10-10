import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from cleaning_action_interfaces.action import CleaningTask


class CleaningActionClient(Node):
    def __init__(self):
        super().__init__('cleaning_action_client')
        self._action_client = ActionClient(self, CleaningTask, 'cleaning_task')
        self.tasks = [
            ("clean_square", 3.0, 0.0, 0.0),
            ("return_home", 0.0, 2.5, 7.6)
        ]
        self.current_task = 0
        self.goal_in_progress = False

    def send_goal(self):
        if self.goal_in_progress:
            return
        if self.current_task >= len(self.tasks):
            self.get_logger().info("All tasks completed!")
            rclpy.shutdown()
            return
        task_type, area_size, target_x, target_y = self.tasks[self.current_task]
        goal_msg = CleaningTask.Goal()
        goal_msg.task_type = task_type
        goal_msg.area_size = area_size
        goal_msg.target_x = target_x
        goal_msg.target_y = target_y

        self.goal_in_progress = True
        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.goal_in_progress = False
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        fb = feedback_msg.feedback
        self.get_logger().info(
            f'Progress: {fb.progress_percent}% '
            f'Cleaned: {fb.current_cleaned_points} '
            f'Pose: ({fb.current_x:.2f}, {fb.current_y:.2f})'
        )

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f'Result: success={result.success}, '
            f'points={result.cleaned_points}, distance={result.total_distance:.2f}'
        )
        self.goal_in_progress = False
        self.current_task += 1
        self.send_goal()


def main(args=None):
    rclpy.init(args=args)
    node = CleaningActionClient()
    node.send_goal()

    rclpy.spin(node)


if __name__ == '__main__':
    main()
