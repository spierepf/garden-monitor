from umqtt.simple import MQTTClient

import etc.mosquitto

c = MQTTClient("garden-monitor", etc.mosquitto.host)
c.connect()
c.publish(b"foo_topic", b"hello")
c.disconnect()

print("Hello World!")
