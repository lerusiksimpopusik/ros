cmake_minimum_required(VERSION 3.8)
project(my_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

add_executable(depth_stop src/depth_stop.cpp)
ament_target_dependencies(depth_stop 
    rclcpp 
    sensor_msgs 
    geometry_msgs 
)
add_executable(circle_movement src/circle_movement.cpp)
add_executable(sinusoid_movement src/sinusoid_movement.cpp)
add_executable(lidar_stop src/lidar_stop.cpp)
ament_target_dependencies(circle_movement rclcpp geometry_msgs)
ament_target_dependencies(sinusoid_movement rclcpp geometry_msgs std_msgs)
ament_target_dependencies(lidar_stop rclcpp sensor_msgs geometry_msgs)
install(TARGETS circle_movement DESTINATION lib/${PROJECT_NAME})
install(TARGETS sinusoid_movement DESTINATION lib/${PROJECT_NAME})
install(TARGETS depth_stop DESTINATION lib/${PROJECT_NAME})
install(TARGETS lidar_stop DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

install(
  DIRECTORY
    urdf
  DESTINATION
    share/${PROJECT_NAME}/
)

install(
  DIRECTORY
    launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

install(
  DIRECTORY
    config/
  DESTINATION share/${PROJECT_NAME}/config
)

install(
  DIRECTORY
    worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

ament_package()
