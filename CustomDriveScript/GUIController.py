import pygame
import rospy
from ackermann_msgs.msg import AckermannDriveStamped

import sys, select, termios, tty

WIDTH = 500
HEIGHT = 500
alive = True
FPS = 60
bg_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = None

turn_rate = 0.05
speed = 2

pub = rospy.Publisher('/vesc/ackermann_cmd_mux/input/teleop', AckermannDriveStamped, queue_size=10)
rospy.init_node('keyop')


def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    run()
    send_message(0, 0)
    pygame.quit()


def handle_events():
    global alive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False


def send_message(speed, turn):
    global pub
    msg = AckermannDriveStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = "base_link"

    msg.drive.speed = speed
    msg.drive.acceleration = 1
    msg.drive.jerk = 1
    msg.drive.steering_angle = turn
    msg.drive.steering_angle_velocity = 1
    pub.publish(msg)


def update():
    global screen, speed
    pubSpeed = 0
    pubTurn = 0
    mouse_pos = pygame.mouse.get_pos()
    if screen.get_rect().collidepoint(mouse_pos):
        pubSpeed = -(mouse_pos[1] - 200) / 200.0
        pubTurn = -(mouse_pos[0] - 200.0) / 800.0
        pubSpeed *= speed
        send_message(pubSpeed, pubTurn)
    else:
        send_message(0, 0)





def render():
    global  bg_color, screen
    screen.fill(bg_color)

    pygame.display.flip()



def run():
    global alive
    while alive:
        clock.tick(FPS)
        handle_events()
        update()
        render()

if __name__ == '__main__':
    main()