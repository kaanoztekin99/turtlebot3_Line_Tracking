# This Script will hold our LIDAR DATAS
import rospy
from sensor_msgs.msg import LaserScan
 
# This function takes the LIDAR datas and make them sense
def lidar_data(veri):

    # to make sense data we created a dictionary which is name areas
    # we added a jpg file to our project that it shows how we created areas with these degrees
    areas = {
        'front1':  min(min(veri.ranges[0:9]), 3.5),
        'front2': min(min(veri.ranges[349:359]), 3.5),
        'front_left':  min(min(veri.ranges[10:49]), 3.5),
        'left':  min(min(veri.ranges[50:89]), 3.5),
        'back':   min(min(veri.ranges[90:268]), 3.5),
        'right':   min(min(veri.ranges[269:308]), 3.5),
        'front_right':   min(min(veri.ranges[309:348]), 3.5),
    }
    
    print (areas)
    
# In this main function we initialized our node which is name tb3_lidar
if __name__ == '__main__':
    
    rospy.init_node('tb3_lidar',anonymous=True)
    
# To geting the LIDAR datas we initialized our Topic name
    rospy.Subscriber('/scan', LaserScan, lidar_data)
# We have callback so we called spin method
    rospy.spin()
