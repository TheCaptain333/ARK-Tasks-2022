#!/usr/bin/env python3
from part1_checker import noDuplicates
import rospy
import std_msgs
from std_msgs.msg import Int64
import numpy as np
import os

pub = rospy.Publisher('/guess_part2', Int64, queue_size=100)

def xCallback(data):
    global x
    x = data.data


def strategy():
    global x
    msg = Int64()
    # Your code here
    # Make sure to publish only distinct n digit numbers else you just increase your number of tries and decrease your score :)
    # If dollarcent = 999 You Win, you can now stop publishing
    # If dollarcent = -999 you probably entered a duplicate number or a number out of range, try again



def play():
    global x
    dollarcent = 0
    rospy.init_node('player1')
    rospy.Subscriber("/check1", Int64, xCallback)
    while not rospy.is_shutdown():
        strategy()





if __name__ == '__main__':
    try:
        play()
    except rospy.ROSInterruptException:
        pass
