import sys
import time

from umqtt.simple import MQTTClient

import etc.mosquitto

def battery_voltage():
  if "linux" == sys.platform:
    return 4.2
  else:
    from machine import Pin
    from machine import ADC
    adc = ADC(Pin(35))
    adc.atten(ADC.ATTN_11DB)
    return 2.0 * (3.6 * adc.read() / 4095.0)

def soil_moisture():
  if "linux" == sys.platform:
    return 0
  else:
    from machine import Pin
    from machine import ADC
    enable = Pin(25, mode=Pin.OUT)
    enable.value(0)

    input = Pin(33, mode=Pin.IN)
    adc = ADC(input)
    adc.atten(ADC.ATTN_11DB)
    input.init(pull=Pin.PULL_DOWN)

    while(adc.read()):
      pass

    input.init(pull=None)
    enable.value(1)
    time.sleep(10)

    return adc.read()


c = MQTTClient("garden-monitor", etc.mosquitto.host)
c.connect()
c.publish(b"/garden-monitor/%s/battery-voltage" % (etc.mosquitto.prefix), b"%f" % (battery_voltage()))
c.publish(b"/garden-monitor/%s/soil-moisture" % (etc.mosquitto.prefix), b"%d" % (soil_moisture()))
c.disconnect()

print("Hello World!")
