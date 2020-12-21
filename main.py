import board
from digitalio import DigitalInOut, Direction
import touchio
import time


# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# added led strips
blink1 = DigitalInOut(board.D2)
blink1.direction = Direction.OUTPUT

blink2 = DigitalInOut(board.D3)
blink2.direction = Direction.OUTPUT

blink3 = DigitalInOut(board.D4)
blink3.direction = Direction.OUTPUT

touched = False
lightsOn = False
counter = 1
cooldownTimer = 0
timer = time.monotonic()
doubleTapTimer = 0
lightAlwaysOn = False
held = False


## Change these if you'd like
blinkTimer = .3  # Change this number to make the blinks last longer or shoter
loopCount = 12  # change this number to changet he number of "blinks" the lights go through when you boop


# Capacitive touch on D1
touch = touchio.TouchIn(board.D1)


######################### HELPER FUNTIONS ########################
def blink(light = 4):
    # Turn off all the lights if they're on
    blink1.value = False
    blink2.value = False
    blink3.value = False
    # Take the value and make one light blinky
    if light == 0:
        blink1.value = True
    if light == 1:
        blink2.value = True
    if light == 2:
        blink3.value = True


######################### STARTUP ################################

# This will run once it's powered up
now = time.monotonic() # Get current time
for x in range(4):  # loop 4 times
    blink1.value = True  # this sets the lights on
    blink2.value = True
    blink3.value = True

    time.sleep(0.1)

    blink1.value = False     # this sets the lights off
    blink2.value = False
    blink3.value = False
    time.sleep(0.1)

######################### MAIN LOOP ##############################

while True:  # This bit of the code will loop forever.
    now = time.monotonic() # Get current time
    
    if (touched == True) and (touch.value == False):  # this checks to see if the nose was booped the last go around but isn't this time
        if counter <= doubleTapTimer and (doubleTapTimer != 0): # If this has happened twice in a second
            lightAlwaysOn  = True  # lights on till another boop
            lightsOn = False
        else:
            doubleTapTimer = counter + 4  # Gives it 4 blinks to wait to see if there's a double tap
        held = False

    touched = touch.value 
    led.value = lightAlwaysOn #led on if lights kept on
    
    if touched: #This runs every time while the nose is booped
        cooldownTimer = counter + loopCount  #This sets the timer point where the lights will turn off again
        if lightsOn == False and lightAlwaysOn == False: #if the lights are off
            print("lightsOn!")
            lightsOn = True
            timer = 1
        elif lightAlwaysOn == True: #This should turn off the lights if it's set to auto on mode
            lightAlwaysOn = False
            blink()
            print("doubletap cancel")
            time.sleep(0.5) #Basically a really hacky debounce.  Otherwise it'll count as a starting boop

    if now - timer > blinkTimer:
      counter = counter + 1
      timer = now
    
    if cooldownTimer < counter:
        lightsOn = False
    
    if lightsOn or lightAlwaysOn:
      blink(counter % 3) #blink one of the three light options
    else:
      blink() #by passing it default values, it'll turn off everything
