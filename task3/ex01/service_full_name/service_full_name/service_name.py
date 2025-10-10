import rclpy
from rclpy.node import Node

from full_name_interfaces.srv import FullNameSumService


class SummFullName(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(FullNameSumService, 'summ_full_name', self.full_name_callback)

    def full_name_callback(self, request, response):
        response.full_name = f"{request.last_name} {request.name} {request.first_name}"
        self.get_logger().info('Incoming request\nlast_name: %s name: %s first_name: %s' % (request.last_name, request.name, request.first_name))

        return response


def main():
    rclpy.init()

    full_name_service = SummFullName()

    rclpy.spin(full_name_service)
    rclpy.shutdown()


if __name__ == '__main__':
    main()