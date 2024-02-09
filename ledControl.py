#!/usr/bin/env python3
#
# Version 5.0
# Version Increment - 506
# Script requires python3
# Written by Robert C Smith II
# Electrical Mentor / FRC Team #4935 T-Rex
# email: robertcsmith719@gmail.com
# This version of the script was written for 2023 Charged Up
# Robot Name: Godzilla

# Import needed python modules used in the script.
import board		# GPIO pin control 
import neopixel		# Allows for addressing neopixel LED strip
import time		# Allows us to use time functions
from time import sleep	# Allows us to use sleep functions
from networktables import NetworkTables	# Needed to read NetworkTables
from networktables.util import ChooserControl	# Needed to read NetworkTables SendableChooser
import syslog	# Allows us to send messages to OS syslog
import os	# Used to exit script cleanly
import logging  # Used to enable logging to syslog and other files

# Grab the current system time at script start
System_time = str(time.strftime("%m%d-%H:%M:%S"))

# Send initial script start message to syslog.
syslog.syslog(syslog.LOG_NOTICE, "LED Control script started.")

# To see messages from networktables, you must setup logging.
# This will allow DEBUG level messages to syslog and configures message logging to a specific output file.
log_file="ledControl-"+System_time+".log"
log_path="/home/trexpi/scripts/logs/"+log_file
logging.basicConfig(filename=log_path, encoding='utf-8', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
syslog.syslog(syslog.LOG_NOTICE, "Log File Created:")

# Set any constants
led_count=60		# Total number of LEDs on neopixels strip
sleep_time = 0.1	# Used for LED blink timing
ip = '10.49.35.2'	# Set IP of NetworkTables host (RoboRIO)
#ip = '10.99.99.2'	# Set IP of NetworkTables host (RoboRIO)
isConnected = False	# Need to set a default robot connection state
gpio_pin1 = board.D18	# Set DIO port to 18 (pin12) for led strip 1 control circuit connection
gpio_pin2 = board.D21	# Set DIO port to 21 (pin40) for led strip 2 control circuit connection
#robot_disabled = [32.0, 34.0]	# Values in FMSInfo table that indicate robot disabled
#robot_enabled = [33.0, 35.0]	# Values in FMSInfo that indicate robot enabled Autonomous=35.0; Teleop=33.0
robot_connected = [32.0, 34.0, 33.0, 35.0] # Indicating that pi sees robot / network tables

# Setup neopixels for LED strip controls.
ORDER = neopixel.GRB
pixels1 = neopixel.NeoPixel(gpio_pin1, led_count, brightness=0.2, pixel_order=ORDER) 
pixels2 = neopixel.NeoPixel(gpio_pin2, led_count, brightness=0.2, pixel_order=ORDER) 

# Godzilla specific constants
gz_sleep_time=0.15
gz_sleep_blink=0.25
gzLoop=0

# Set LED color codes.
off=(0,0,0)
red=(255,0,0)
yellow=(255,175,0)
green=(0,255,0)
aqua=(0,255,255)
blue=(0,0,255)
purple=(255,0,255)
white=(255,255,255)
gz=(75,75,255)
color=(gz)	# Sets a default color


# Define LED Control functions.
def function_setcolor(color):
	pixels1.fill(color)
	pixels2.fill(color)

def function_off_p1():
	pixels1.fill(off)
 
def function_off_p2():
	pixels2.fill(off)
 
def function_off_all():
	pixels1.fill(off)
	pixels2.fill(off)

def function_blink(color, sleep_time):
	for b in range(5):
		pixels1[b] = (color)
		function_off_p1()
		sleep(sleep_time)
		pixels1.fill(color)
		sleep(sleep_time)

def function_drive_red():
	for d in range(0,30):
		pixels1[d] = (red)
		pixels2[d] = (off)
		pixels1.write()
		pixels2.write()
        
def function_drive_blue():
    for d in range(0,30):
        pixels2[d] = (blue)
        pixels1[d] = (off)
        pixels2.write()
        pixels1.write()
        
def function_cone():
    for r in range(30,60):
        pixels1[r] = (yellow)
        pixels2[r] = (yellow)
        pixels1.write()
        pixels2.write()
        
def function_cube():
    for r in range(30,60):
        pixels1[r] = (purple)
        pixels2[r] = (purple)
        pixels1.write()
        pixels2.write()

def function_connected():
	pixels1.fill(gz)
	pixels2.fill(gz)

def function_godzilla(color):
    global gzLoop
    gzLoop +=1
    if gzLoop > 4:
        pixels1.fill(gz)
        pixels2.fill(gz)
    else:
        pixels1.fill(off)
        pixels2.fill(off)
        for c in range(led_count):
            pixels_gz = neopixel.NeoPixel(gpio_pin1, c, brightness=0.5)
            pixels_gz2 = neopixel.NeoPixel(gpio_pin2, c, brightness=0.5)
            pixels_gz.fill(color)
            pixels_gz2.fill(color)
            sleep(gz_sleep_time)
        for b in range(3):
            pixels1[b] = (color)
            pixels2[b] = (color)
            pixels1.fill(off)
            pixels2.fill(off)
            sleep(gz_sleep_blink)
            pixels1.fill(color)
            pixels2.fill(color)
            sleep(gz_sleep_blink)
        sleep(4)
        return gzLoop

# Initialize NetworkTables connection and listeners.
NetworkTables.initialize(server=ip)

def valueChanged(table, key, value, isNew):
	print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

def connectionListener(connected, info):
	print(info, "; Connected=%s" % connected)
	global isConnected
	isConnected = (connected)
	return isConnected

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# Watch NetworkTables "FMSInfo" for changes.
fms = NetworkTables.getTable("FMSInfo")
# Read the "FMSControlData" table for robot status (disabled, auto, teleop)
robot_status = fms.getEntry("FMSControlData")
# Listener to detect changes in robot state.
fms.addEntryListener(valueChanged)

# Watch NetworkTables "SmartDashboard" for changes
sd = NetworkTables.getTable("SmartDashboard/Arm")
# Read the "LED_Control" entry for LED control message
#sd_ledControl = sd.getBoolean("isCube",False)
sd_ledControl = sd.getEntry("isCube")
sd_ledControlDrive = sd.getEntry("isBatterySide")
sd_ledControlAuto = sd.getEntry("isAutonomous")
#sd.addEntryListener(valueChanged)


# Start loops with all LEDs off
function_off_all()


# Wait for NetworkTables Read before looping.
# Otherwise, script exits immediately.
time.sleep(0.5)

# If robot is not connected, make sure status LEDs are set to RED.
# Clear any other statuses first.
# LED blinking is based on the duration of the led listener service.
# Also used as an indicator that the led service is running on the PI.
# If no connection to NetworkTables is found, exit script and wait for retry.
# Script retry duration is set based on PI OS service (5 seconds for T-Rex).
if (robot_status.value == None):
	function_off_all()
	for n in range(0, 61, 3):
		pixels1[n]=(red)
		pixels2[n]=(red)
	syslog.syslog(syslog.LOG_NOTICE, "Robot NOT CONNECTED.")
	os._exit(1)

# Loop that reads NetworkTables and controls LEDs.
# Scripts exits when it detects a lost robot connection.
# ////////////////////////////////////////////////////////////
while True:
	# LED Controls
	if sd_ledControlAuto.value == "GODZILLA":
		color=(gz)
		function_godzilla(color)
		print("Color set by godzilla: ", color)
		logging.info('Color set by godzilla: %s', color)
	else:
		if sd_ledControl.value == "cone":
			function_cone()
			print("Color set by cone: ")
			logging.info('Color set by cone: %s')
		elif sd_ledControl.value == "cube":
			function_cube()
			print("Color set by cube: ")
			logging.info('Color set by cube: %s')
		else:
			color=(gz)
			function_setcolor(color)
			print("Color not set by Robot Code: ", color)
			logging.warning('Color not set by Robot Code: %s', color)
		if sd_ledControlDrive.value == "compressor":
			function_drive_blue()
			print("Color set by drive: ", color)
			logging.info('Color set by drive: %s', color)
		elif sd_ledControlDrive.value == "battery":
			function_drive_red()
			print("Color set by drive: ", color)
			logging.info('Color set by drive: %s', color)
		else:
			color=(gz)
			function_setcolor(color)
			print("Color not set by Robot Code: ", color)
			logging.info('Color not set by Robot Code: %s', color)
	if isConnected == False:
			syslog.syslog(syslog.LOG_NOTICE, "LOST Connection to Robot.")
			logging.error('LOST Connection to Robot.')
			os._exit(1)
	sd.putNumberArray("LED Color set to: ", color)
	logging.info('LED Color set to: %s', color)
	time.sleep(0.1)

# Syslog message that will be sent only if script is exited outside of loops.
syslog.syslog(syslog.LOG_NOTICE, "LED Control script ended without using exits.")
function_off_p1()
function_off_p2()
