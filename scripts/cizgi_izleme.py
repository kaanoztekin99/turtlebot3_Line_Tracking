# This script is wrote for our bot is to follow the yellow line
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

class Cizgi:

    # Our constructor __init__
    def __init__(self):
        
        self.bridge = cv_bridge.CvBridge()
        
        self.image_sub = rospy.Subscriber('camera/image',Image, self.func)
        # topic that we are going to take the camera view
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        # topic that we are going to publish with type of Twist
        
        self.twist = Twist()

    def func(self, ros_goruntu):
        
        # we are going to transform ros_goruntu to the OpenCV form
        cv_goruntu = self.bridge.imgmsg_to_cv2(ros_goruntu,'bgr8')
        
        hsv_goruntu = cv2.cvtColor(cv_goruntu, cv2.COLOR_BGR2HSV)

	# lower and upper yellow variables are our edge values for robot
        lower_yellow = numpy.array([ 10, 10, 10])
        upper_yellow = numpy.array([255, 255, 250])
        
        # Masking : display images different from the yellow line
        mask = cv2.inRange(hsv_goruntu, lower_yellow, upper_yellow)

        cv2.imshow('maske', mask)
	# after the masking operation new window will open and shows the remain part of the image        
	# our height weight and depth values
        h, w, d = hsv_goruntu.shape
        
        search_top = 3*h/4
        search_bot = 3*h/4 + 20
        
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        # We have applied the cropping process on the image we masked. 
        cv2.imshow('kirpilmis_maske', mask)
        # our new window and image
        M = cv2.moments(mask)
            
        if M['m00'] > 0:
            # The process of finding the midpoint of the detected yellow line 
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # The x and y points are the center point of our line. 
            cv2.circle(cv_goruntu, (cx, cy), 20, (0,0,255), -1)
            # The process of placing a red dot at the midpoint of the line. 
            # So we used our circle method
            err = cx - w/2
        
        self.twist.linear.x = 0.1
        # Our turn rate -float(err)/100 --> P controle (Proportional)
        self.twist.angular.z = -float(err) / 100
        self.cmd_vel_pub.publish(self.twist)
	# We published out motion part while sending Twist object
        cv2.imshow('cizgi izleme', cv_goruntu)
        # Our windows name is : cizgi_izleme
        cv2.waitKey(3)

if __name__ == "__main__":

    rospy.init_node('cizgi_izleme') 
    obje = Cizgi()
    rospy.spin()
