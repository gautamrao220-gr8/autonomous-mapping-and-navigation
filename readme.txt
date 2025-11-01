SETUP INSTRUCTIONS:
1. Extract the bgr_ws directory which contain all the packages.
2. Open terminal
3. Install the required packages:
	sudo apt install ros-jazzy-xacro
	sudo apt install ros-jazzy-robot-state-publisher
	sudo apt install ros-jazzy-joint-state-publisher
	sudo apt install ros-jazzy-joint-state-publisher-gui
	sudo apt install ros-jazzy-teleop-twist-keyboard
	sudo apt install ros-jazzy-twist-mux
	sudo apt install ros-jazzy-twist-stamper
	sudo apt install ros-jazzy-topic-tools
	sudo apt install ros-jazzy-tf2-tools
	sudo apt install ros-jazzy-tf-transformations
	sudo apt install ros-jazzy-rqt
	sudo apt install ros-jazzy-rqt-graph
	sudo apt install ros-jazzy-rqt-tf-tree
	sudo apt install ros-jazzy-rqt-image-view
	sudo apt install ros-jazzy-ros-gz
	sudo apt install ros-jazzy-ros-gz-bridge
	sudo apt install ros-jazzy-ros-gz-sim
	sudo apt install ros-jazzy-ros2-control
	sudo apt install ros-jazzy-ros2-controllers
	sudo apt install ros-jazzy-gz-ros2-control
	sudo apt install ros-jazzy-gz-ros2-control-demos
	sudo apt install ros-jazzy-navigation2
	sudo apt install ros-jazzy-nav2-bringup
	sudo apt install ros-jazzy-slam-toolbox
	sudo apt install ros-jazzy-interactive-markers
	sudo apt install ros-jazzy-dynamixel-sdk
	sudo apt install ros-jazzy-hardware-interface
	sudo apt install ros-jazzy-nav2-msgs
	sudo apt install ros-jazzy-nav2-costmap-2d
	sudo apt install ros-jazzy-nav2-map-server
	sudo apt install ros-jazzy-nav2-bt-navigator
	sudo apt install ros-jazzy-nav2-bringup
	sudo apt install ros-jazzy-interactive-marker-twist-server
	sudo apt install ros-jazzy-cartographer-ros
	

4. Change directory to bgr_ws [ex:cd home/bgr/bgr_ws]
5. inside bgr_ws run: colcon build
6. Source the directory: source install/setup.bash
7. run: export GZ_SIM_RESOURCE_PATH=$HOME/ros_ws/src/gazebo_models
8.spawn single robot: ros2 launch bme_ros2_navigation spawn_robot.launch.py
9. mapping: ros2 launch bme_ros2_navigation mapping.launch.py
10. spawning multiple robot: ros2 launch bme_ros2_navigation multi_robot_spawn.launch.py 
11. navigation: ros2 launch bme_ros2_navigation multi_robot_navigation.launch.py 
