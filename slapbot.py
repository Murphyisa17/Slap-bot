from machine import Pin, ADC, I2C
import utime
from pico_i2c_lcd import I2cLcd

# ==================================
# LCD SETUP
# ==================================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def show(line1="", line2=""):
    lcd.move_to(0, 0)
    lcd.putstr(str(line1)[:16].ljust(16))
    lcd.move_to(0, 1)
    lcd.putstr(str(line2)[:16].ljust(16))

# ==================================
# CD4051 MULTIPLEXER
# ==================================
s0 = Pin(2, Pin.OUT)
s1 = Pin(3, Pin.OUT)
s2 = Pin(4, Pin.OUT)

adc = ADC(26)

FACE1_CH = 0
FACE2_CH = 1
CHIN_CH = 3

def read_channel(ch):
    s0.value(ch & 1)
    s1.value((ch >> 1) & 1)
    s2.value((ch >> 2) & 1)

    utime.sleep_ms(5)
    adc.read_u16()
    utime.sleep_ms(2)
    return adc.read_u16()

def average_channel(ch, samples=15):
    total = 0
    for i in range(samples):
        total += read_channel(ch)
    return total // samples

# ==================================
# SCORING SETTINGS
# ==================================
FACE_THRESHOLD = 1200
CHIN_THRESHOLD = 9000
CHIN_MARGIN = 3000

DIVISOR = 150
HIT_WINDOW_MS = 1000
HOLD_MS = 3000

# ==================================
# START PROGRAM
# ==================================
show("SLAP BOT", "Initializing...")
utime.sleep(2)

# CSV header for MATLAB
print("time_ms,face1,face2,chin,score")

start_time = utime.ticks_ms()

while True:

    # --------------------------
    # BASELINE CALIBRATION
    # --------------------------
    show("Calibrating...", "Do not touch")
    utime.sleep_ms(700)

    base_face1 = average_channel(FACE1_CH)
    base_face2 = average_channel(FACE2_CH)
    base_chin = average_channel(CHIN_CH)

    # --------------------------
    # COUNTDOWN
    # --------------------------
    for n in [3, 2, 1]:
        show("GET READY!", "Hit in: {}".format(n))
        utime.sleep(1)
