import network
import time

def _connect(sta_if, essid, password=None):
  sta_if.connect(essid, password)
  while sta_if.status() == network.STAT_CONNECTING:
    time.sleep_ms(100)
  return sta_if.isconnected()

def connect(aps={}):
  sta_if = network.WLAN(network.STA_IF)
  if sta_if.isconnected():
    return sta_if.ifconfig()

  sta_if.active(True)
  scan = sta_if.scan()
  for ap in scan:
    essid = ap[0].decode('utf-8')
    authmode = ap[4]
    if aps and essid in aps or not aps and 0==authmode:
      if _connect(sta_if, essid, aps[essid]):
        return sta_if.ifconfig()
  return None
