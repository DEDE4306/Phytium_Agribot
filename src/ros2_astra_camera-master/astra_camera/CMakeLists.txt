cmake_minimum_required(VERSION 3.8)
set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")  # 让可执行文件在安装后从../lib查找依赖
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
project(astra_camera)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}  -fPIC -g")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC -O3")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC -g")
set(CMAKE_BUILD_TYPE "Debug")
if (CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif ()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(ament_index_cpp REQUIRED)
find_package(astra_camera_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(camera_info_manager REQUIRED)
find_package(class_loader REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(message_filters REQUIRED)
find_package(camera_info_manager REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(image_geometry REQUIRED)
find_package(image_publisher REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rcutils REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(PkgConfig REQUIRED)

pkg_search_module(LIBUVC REQUIRED libuvc)
if (NOT LIBUVC_FOUND)
  message(FATAL_ERROR "libuvc is not found")
endif ()
pkg_search_module(GLOG REQUIRED libglog)

if (NOT GLOG_FOUND)
  message(FATAL_ERROR "glog is not found")
endif ()


execute_process(COMMAND uname -m OUTPUT_VARIABLE MACHINES)
execute_process(COMMAND getconf LONG_BIT OUTPUT_VARIABLE MACHINES_BIT)
message(STATUS "ORRBEC Machine : ${MACHINES}")
message(STATUS "ORRBEC Machine Bits : ${MACHINES_BIT}")

if ((${MACHINES} MATCHES "x86_64") AND (${MACHINES_BIT} MATCHES "64"))
  set(HOST_PLATFORM "x64")
elseif (${MACHINES} MATCHES "arm")
  set(HOST_PLATFORM "arm")
elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "64"))
  set(HOST_PLATFORM "arm64")
elseif ((${MACHINES} MATCHES "aarch64") AND (${MACHINES_BIT} MATCHES "32"))
  set(HOST_PLATFORM "arm")
endif ()


message(STATUS "ORRBEC : ${HOST_PLATFORM}")
set(ORBBEC_OPENNI2_REDIST
  "${CMAKE_CURRENT_SOURCE_DIR}/openni2_redist/${HOST_PLATFORM}")

set(dependencies
  ament_index_cpp
  astra_camera_msgs
  builtin_interfaces
  class_loader
  cv_bridge
  Eigen3
  image_geometry
  image_publisher
  image_transport
  rclcpp
  rclcpp_components
  rcutils
  sensor_msgs
  std_msgs
  std_srvs
  tf2
  tf2_msgs
  tf2_ros
  tf2_sensor_msgs
  message_filters
  camera_info_manager
  )

add_library(${PROJECT_NAME} SHARED
  src/point_cloud_proc/point_cloud_xyz.cpp
  src/point_cloud_proc/point_cloud_xyzrgb.cpp
  src/ob_context.cpp
  src/dynamic_params.cpp
  src/ob_camera_info.cpp
  src/ob_timer_filter.cpp
  src/ob_camera_node_factory.cpp
  src/ob_camera_node.cpp
  src/ros_param_backend.cpp
  src/ros_service.cpp
  src/utils.cpp
  src/uvc_camera_driver.cpp
  )

target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDED_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${GLOG__INCLUDE_DIRS}
  )

ament_target_dependencies(${PROJECT_NAME}
  ${dependencies}
  )

target_link_libraries(${PROJECT_NAME}
  ${OpenCV_LIBS}
  Eigen3::Eigen
  ${GLOG_LIBRARIES}
  ${LIBUVC_LIBRARIES}
  "${ORBBEC_OPENNI2_REDIST}/libOpenNI2_astra.so"
  )

add_executable(${PROJECT_NAME}_node
  src/main.cpp
  )

target_include_directories(${PROJECT_NAME}_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDED_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${GLOG__INCLUDE_DIRS}
  )

ament_target_dependencies(${PROJECT_NAME}_node
  ${dependencies}
  )

target_link_libraries(${PROJECT_NAME}_node
  ${OpenCV_LIBS}
  Eigen3::Eigen
  ${GLOG_LIBRARIES}
  ${LIBUVC_LIBRARIES}
  "${ORBBEC_OPENNI2_REDIST}/libOpenNI2_astra.so"
  ${PROJECT_NAME}
  )

add_executable(list_devices_node
  src/list_devices_node.cpp
  )
target_include_directories(list_devices_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDED_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${GLOG__INCLUDE_DIRS}
  )

ament_target_dependencies(list_devices_node
  ${dependencies}
  )
target_link_libraries(list_devices_node
  ${OpenCV_LIBS}
  Eigen3::Eigen
  ${GLOG_LIBRARIES}
  ${LIBUVC_LIBRARIES}
  "${ORBBEC_OPENNI2_REDIST}/libOpenNI2_astra.so"
  ${PROJECT_NAME}
  )

add_executable(clean_shm_node
  src/clean_up_shm_node.cpp
  )

target_include_directories(clean_shm_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDED_DIRS}
  ${LIBUVC_INCLUDE_DIRS}
  ${GLOG__INCLUDE_DIRS}
  )

ament_target_dependencies(clean_shm_node
  ${dependencies}
  )

target_link_libraries(clean_shm_node
  ${OpenCV_LIBS}
  Eigen3::Eigen
  ${GLOG_LIBRARIES}
  ${LIBUVC_LIBRARIES}
  "${ORBBEC_OPENNI2_REDIST}/libOpenNI2_astra.so"
  ${PROJECT_NAME}
  )

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
  )

install(FILES ${ORBBEC_OPENNI2_REDIST}/libOpenNI2_astra.so
  DESTINATION lib/
  )


install(DIRECTORY ${ORBBEC_OPENNI2_REDIST}/OpenNI2
  DESTINATION lib/
  )

install(TARGETS list_devices_node
  clean_shm_node
  ${PROJECT_NAME}_node
  DESTINATION lib/${PROJECT_NAME}/
  )

install(
  DIRECTORY include/
  DESTINATION include
)

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
  )


if (BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif ()
ament_export_include_directories(include)
ament_export_libraries(${PROJECT_NAME})
ament_export_dependencies(${dependencies})

ament_package()
