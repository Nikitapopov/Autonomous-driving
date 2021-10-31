#! /usr/bin/python

import rospy
import time
import math
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class TurtleHunterBot:
    def __init__(self):
        rospy.Service('/spawn', Spawn, self.spawn_callback)
        self.r = rospy.Rate(0.33)
        self.x_turtle1 = 0
        self.y_turtle1 = 0
        self.x_hunter = 0
        self.y_hunter = 0

        self.vel_x = 0
        self.vel_y = 0
        self.angle_prev = 0

        rospy.Subscriber('/turtle1/pose', Pose, self.update_turtle1_pose)
        rospy.Subscriber('/turtle1/cmd_vel', Twist, self.move_to_victim)
        rospy.Subscriber('/hunter/pose', Pose, self.update_pose)
        self.pub1 = rospy.Publisher('/hunter/cmd_vel', Twist, queue_size=1)

    def move_to_victim(self, msg):
        vel_msg = Twist()

        self.vel_x = self.x_turtle1 - self.x_hunter
        self.vel_y = self.y_turtle1 - self.y_hunter

        angle = math.atan2(self.vel_y, self.vel_x)
        magnitude = math.sqrt(pow(self.vel_x, 2) + pow(self.vel_y, 2))

        vel_msg.angular.z = angle - self.angle_prev
        vel_msg.linear.x = 0
        self.angle_prev = angle
        self.pub1.publish(vel_msg)
        self.r.sleep()

        vel_msg.angular.z = 0
        vel_msg.linear.x = magnitude * 0.5
        self.pub1.publish(vel_msg)
        self.r.sleep()

    def update_turtle1_pose(self, msg):
        self.x_turtle1 = msg.x
        self.y_turtle1 = msg.y

    def update_pose(self, msg):
        self.x_hunter = msg.x
        self.y_hunter = msg.y


rospy.init_node('spawn_handler')
TurtleHunterBot()
rospy.spin()
