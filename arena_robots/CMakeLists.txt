cmake_minimum_required(VERSION 3.5)
project(arena_robots)

find_package(ament_cmake REQUIRED)


install(
  DIRECTORY robots/
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
