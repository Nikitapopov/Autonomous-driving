#! /usr/bin/python

import rospy
import random
import math
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.msg import Pose


class TurtleBot:
    def __init__(self):
        rospy.init_node('spawn_caller')
        rospy.wait_for_service('/spawn')
        self.initHunter()

    def initHunter(self):
        spawn_func = rospy.ServiceProxy('/spawn', Spawn)
        spawn_func(0.0, 0.0, 0.0, 'hunter')

TurtleBot()
rospy.spin()
