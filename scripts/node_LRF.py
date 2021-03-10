#!/usr/bin/env python3
import board
import busio
import adafruit_lidarlite
import rospy
from sensor_msgs.msg import Range

if __name__ == '__main__':
    # init ros node & publisher
    rospy.init_node('LRF_bridge')
    pub_LRF = rospy.Publisher('/mavros/px4flow/ground_distance', Range, queue_size=2)

    # init LRF sensor configuration
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_lidarlite.LIDARLite(i2c)

    # init msg
    msg = Range()

    # set topic frequency
    rate = rospy.Rate(30.0)
    while True:
        try:
            msg.header.stamp = rospy.Time.now()
            msg.range = sensor.distance / 100.0
            pub_LRF.publish(msg)
        except RuntimeError as e:
            print(e)

        rate.sleep()