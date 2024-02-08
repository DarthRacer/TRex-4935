# RaspberryPi-4935
Initial repo for raspberryPi configs and control scripts for T-Rex #4935

T-Rex has tackled the task of controlling NeoPixel LED strips using a co-processor.

Our co-processor of choice is a Raspberry Pi 3 V1.2

We are running a custom python3 script to control the LEDs.

The script watches NetworkTables for command instructions.

It also runs as a service on the Pi to ensure it is always running.

It does not require any connections once configured except ethernet network connection to the robo rio.

Initial configuration of the pi and custom scripts authored by:

Robert C Smith II - mentor

email: robertcsmith719@gmail.com
