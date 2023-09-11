from machine import Pin
from machine import ADC
from time import sleep
from machine import deepsleep

pin = Pin(34)
adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)
button_pin = Pin(0, Pin.IN)

val1=adc.read()
val2=3.3*val1/4095
print('Raw value: ',val1,' and voltage: ',val2)

if button_pin.value()==1:
    deepsleep(1000)