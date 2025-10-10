import sys

import rclpy
from rclpy.node import Node

from full_name_interfaces.srv import FullNameSumService

class SummFullNameClientAsync(Node):

    def __init__(self):
        super().__init__('summ_full_name_client_async')
        self.cli = self.create_client(FullNameSumService, 'summ_full_name')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = FullNameSumService.Request()

    def send_request(self, last_name, name, first_name):
        self.req.last_name = last_name
        self.req.name = name
        self.req.first_name = first_name
        return self.cli.call_async(self.req)


def main():
    rclpy.init()

    full_name_client = SummFullNameClientAsync()
    future = full_name_client.send_request(sys.argv[1], sys.argv[2], sys.argv[3])
    rclpy.spin_until_future_complete(full_name_client, future)
    response = future.result()
    full_name_client.get_logger().info(
        'Result of summ full name: for %s + %s + %s = %s' %
        (sys.argv[1], sys.argv[2], sys.argv[3], response.full_name))

    full_name_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()