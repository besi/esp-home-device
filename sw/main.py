import time
import machine

sleep_interval_s = 5

# Setup AM2320 temperature sensor
# mip.install("github:mcauser/micropython-am2320/am2320.py")
import am2320 # VCC - DATA - GND - CLK
i2c = I2C(1, freq=100 * 1000)
sensor = am2320.AM2320(i2c)

# Setup SSD1306 OLED Display
# mip.install("github:RuiSantosdotme/ESP-MicroPython/code/Others/OLED/ssd1306.py")
from machine import Pin, SoftI2C, I2C
import ssd1306

def updateDisplay(temp, hum):
    global oled
    oled.fill(0)
    oled.text(f'Temp. {temp}', 0, 0)
    oled.text(f'Hum.  {hum}', 0, 10)
    oled.show()

# Setup OLED
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


# setup fourbutton remote
button_a = 18
button_b = 23
button_c = 19
button_d = 22

def buttonPressed(pin):
    global button_a, button_b, button_c, button_d
    if pin == Pin(button_a):   print("A")
    elif pin == Pin(button_b): print("B")
    elif pin == Pin(button_c): print("C")
    elif pin == Pin(button_d): print("D")

Pin(button_a).irq(trigger=Pin.IRQ_FALLING, handler=buttonPressed)
Pin(button_b).irq(trigger=Pin.IRQ_FALLING, handler=buttonPressed)
Pin(button_c).irq(trigger=Pin.IRQ_FALLING, handler=buttonPressed)
Pin(button_d).irq(trigger=Pin.IRQ_FALLING, handler=buttonPressed)

while True:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    updateDisplay(temp, hum)
    print(f"temp: {temp}, hum: {hum}")
    time.sleep(sleep_interval_s)
