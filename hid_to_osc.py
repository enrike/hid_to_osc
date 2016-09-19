"""
HID to OSC converter by www.ixi-audio.net

license: GPL

Receives HID (joystick, gamepad) events and broadcasts them via OSC on IP:PORT
Based on pygame, the python SDL implementation
"""

import pygame
from pygame.locals import *
from simpleOSC import *


SIZE = 200,100
IP = "127.0.0.1"
PORT = 9001

initOSCClient(IP, PORT)


### listen my own messages. sometimes it is useful for testing #
##initOSCServer(IP, PORT) # takes args : ip, port, mode --> 0 for basic server, 1 for threading server, 2 for forking server
##from OSC import getUrlStr
##def report(addr, tags, data, source):
##    print "-"*20
##    print "received osc msg from %s" % getUrlStr(source)
##    print "addr : %s" % addr
##    print "typetags :%s" % tags
##    print "data is : %s" % data
##    print "-"*20
##setOSCHandler("/axis", report)t)
##setOSCHandler("/buttonDown", report)
##setOSCHandler("/buttonUp", report)
##setOSCHandler("/ballMotion", report)
##setOSCHandler("/hatMotion", report)
##startOSCServer() # and now set server into action
################################################################


# HID to OSC connections
def axisMotion(hid, axis, val):
    print "HID device %s / axis %s / value %s" % (hid, axis, val)
    sendOSCMsg("/axis/%s" % axis, [val])

def buttonDown(hid, button):
    print "HID device %s / buttonDown %s " % (hid, button)
    sendOSCMsg("/buttonDown/%s" % button, [button])

def buttonUp(hid, button):
    print "HID device %s / buttonUp %s " % (hid, button)
    sendOSCMsg("/buttonUp/%s" % button, [button])

def ballMotion(hid, ball, val):
    print "HID device %s / ball %s / value %s" % (hid, ball, val)
    sendOSCMsg("/ballMotion/%s" % ball, [val])
    
def hatMotion(hid, hat, val):
    print "HID device %s / hat %s / value %s" % (hid, hat, val)
    sendOSCMsg("/hatMotion/%s" % hat, [val])

             
# INITIALISE #
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode(SIZE, OPENGL | DOUBLEBUF) # HWSURFACE
pygame.display.set_caption("HID to OSC on %s:%s" % (IP, PORT))
clock = pygame.time.Clock()

# device initialisation
try: 
    pygame.joystick.init() # init main joystick device system
    for n in range(pygame.joystick.get_count()): #
        stick = pygame.joystick.Joystick(n)
        stick.init() 
        # report joystick charateristics #
        print '-'*20
        print 'Enabled HID device: %s' % stick.get_name()
        print 'it has the following controls:'
        print '--> buttons: %s' % stick.get_numbuttons()
        print '--> balls: %s' % stick.get_numballs()
        print '--> axes: %s' % stick.get_numaxes()
        print '--> hats: %s' % stick.get_numhats()
        print '-'*20
except pygame.error:
    print 'no HID device found.'



# MAIN LOOP #

running = 1
while running :   
    for e in pygame.event.get(): 
        if e.type == QUIT:
            running = 0
            closeOSC()
        elif e.type == JOYAXISMOTION: # 7
            axisMotion(e.joy, e.axis, e.value)

        elif e.type == JOYBALLMOTION: # 8
            ballMotion(e.joy, e.ball, e.value)

        elif e.type == JOYHATMOTION: # 9
            hatMotion(e.joy, e.hat, e.value)

        elif e.type == JOYBUTTONDOWN: # 10
            buttonDown(e.joy, e.button)

        elif e.type == JOYBUTTONUP: # 11
            buttonUp(e.joy, e.button)
            
    clock.tick(25) # FPS
    pygame.display.flip()


# QUIT
pygame.quit() 
closeOSC()
print "done"
