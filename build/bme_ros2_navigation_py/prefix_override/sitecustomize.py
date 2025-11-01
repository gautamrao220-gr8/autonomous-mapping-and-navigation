import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bgr/bgr_ws/install/bme_ros2_navigation_py'
