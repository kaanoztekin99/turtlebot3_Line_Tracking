# This scripts is just the move the robot autonomously
 
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
 
def lidar_data(veri):

	# our distance variables
    areas = {
        
        'front1':  min(min(veri.ranges[0:9]), 30),
        'front2': min(min(veri.ranges[349:359]), 30),
        'front_left':  min(min(veri.ranges[10:49]), 30),
        'left':  min(min(veri.ranges[50:89]), 30),
        'back':   min(min(veri.ranges[90:268]), 30),
        'right':   min(min(veri.ranges[269:308]), 30),
        'front_right':   min(min(veri.ranges[309:348]), 30),
    }
    
    print (areas)
    move(areas)
    
def move(areas):
 
    if areas['front1'] and areas['front2'] > 0.8:

        hiz = 0.8
        
        if areas['front_right'] - areas['front_left'] > 1.0:    
            
            print ('TURN:RIGHT') 
            # robot is slow down while our robot was turning  
            hiz = 0.4
            donus = -0.4
                                 
        elif areas['front_left'] - areas['front_right'] > 1.0:    
            
            print ('TURN:LEFT')
            hiz = 0.4
            donus = 0.4
        
        else:
            print('LEFT:0')
            hiz = 0.8
            donus = 0.0
                         
    else: 
        
        print('STOP')
        hiz = 0.0
        donus = 0.0

    obje.linear.x = hiz
    obje.angular.z = donus
    pub.publish(obje)

def stop():
 
    rospy.loginfo("robot is stopped !")
    pub.publish(Twist())

if __name__ == '__main__':
  
    # we created a new node called tb3_otonom
    rospy.init_node('tb3_otonom',anonymous=True)
    # we specified the topic that we want to subscribe
    rospy.Subscriber('/scan', LaserScan, lidar_data)
    # in /scan topic we can get LIDAR datas
    rospy.loginfo("To end: CTRL + C")
    rospy.on_shutdown(stop)

    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    # with cmd_vel topic we created Twitst object and specified size of the queue
    
    # to get move function arguments we created our object from Twist class
    obje = Twist()

    rospy.spin()
