from machine import Pin, ADC
from time import sleep

led = Pin("LED", Pin.OUT)
adc = ADC(Pin(28))   # GP28 (ADC2)

while True:
    raw = adc.read_u16()                # 0–65535
    voltage = (raw / 65535) * 3.3       # Convert to volts
    
    print(raw)    # <- This line will auto-plot in Thonny
    
    # Optional LED indicator:
    if voltage > 1.5:
        led.on()
    else:
        led.off()
    
    sleep(0.1)
