# This repository will guide you on how to control neo-pixel through can bus fd using 2 pi 5

## Every tools necesary for this project.
+ 2 pi 5
+ 2 can bus fd
+ Neo-pixel (prefer neo-pixel with 60 leds)
+ jumper wires

## Wiring
As can bus fd is a raspberry hat there for we only need to connect the hat directly to both of pi 5.
However, enable for can comunication, consider following the connection guide below.
|                Can Bus FD                    |               Can Bus FD            |
|----------------------------------------------|-------------------------------------|
| (on the same pi that connected to neo-pixel) |(the one that doesn't have neo-pixel)| 
|----------------------------------------------|-------------------------------------|
|                  can0_H                      |                can_1_H              |
|                  can0_L                      |                can_1_L              |

## Workflow
There is 1 pi 5 with connected to both can hat and neo-pixel. That exact pi will be the one that will contineously wait for can signals (which is sent by another pi 5 with connection to can hat) to be seen which depend of the type signal, neo-pixel's state will changed based on it.

## Configure both pi 5 to enable can comunication
Doing all the steps below on both pi 5
### Step 1: 
Open terminal and run:

<pre> sudo raspi-config </pre>

Choose **interface option** -> **SPI** -> **enable**.
When done, reboot the computer

### Step 2: 
Change config.txt
<pre> sudo nano /boot/config.txt </pre>

Adding things below on config.txt
<pre> dtparam=spi=on

# CAN FD Channel 1 (can0)
dtoverlay=mcp251xfd,spi0-0,oscillator=40000000,interrupt=23

# CAN FD Channel 2 (can1)
dtoverlay=mcp251xfd,spi0-1,oscillator=40000000,interrupt=24
</pre>

Reboot the computer, when done to save the changes

### Step 3:
Execute the code below in both pi 5
<pre>
  sudo ip link set can0 up type can bitrate 1000000   dbitrate 8000000 restart-ms 1000 berr-reporting on fd on
  sudo ifconfig can0 txqueuelen 65536
</pre>

**Warning**: if your sending can pi 5 is running unfamiliar linux distro then that pi 5 then you only need to execute the code above to define bitrate for can0, no need to do step 1 and step 2 on that pi 5.

### Step 4: 
Testing if you receive can signals
Execute the command below on one pi:
<pre>
  candump can0
</pre>
Then, open the terminal of another pi then execute the command below:
<pre>
  cangen can0
</pre>

** Expected result **: the pi that executed the "candump" command will contineously receive can signal from the remaining pi

## Running the code:
But before running the code you need to install required libraries.
<pre>
  pip install python-can adafruit-circuitpython-neopixel adafruit-blinka
</pre>
Then on the raspberry that connected to neo-pixel execute the code name * neo_pixel.py *

Move to the other pi terminal run the following command:
<pre>
  cansend can0 123#01.ff.ff.ff.ff
  # The first 3 numbers actually have to power to dectect neo-pixel behavior. 
  # 01 is for On, 00 is for Off.
  # ff.ff.ff will be the element that define what colour the neo-pixel will display
  # The final on ff is for the intensity from 0 - 255
</pre>

There is another file on the repository named "pi_send_can_automatically.py"
This file will help pi 5 to automatically send can signal, which will turn on and off neo-pixel automacially.
