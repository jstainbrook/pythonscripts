#!/usr/bin/env python

import time
from sys import exit
try:
  import requests
except ImportError:
  exit('This script requires the requests module')

import unicornhat as unicorn

print("""Connects to the Cheerlight API and retrieves current JSON for color
""")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.5)
width,height=unicorn.get_shape()

def hex_to_rgb(col_hex):
    """Convert a hex colour to an RGB tuple."""
    col_hex = col_hex.lstrip('#')
    return bytearray.fromhex(col_hex)

while True:
    r = requests.get('http://api.thingspeak.com/channels/1417/field/2/last.json', timeout=2)
    json = r.json()

    if 'field2' not in json:
        print('Error {status}: {error}'.format(status=json['status'], error=json['error']))
        time.sleep(5)
        continue

    r, g, b = hex_to_rgb(json['field2'])

    unicorn.set_all(r, g, b)

    unicorn.show()

    time.sleep(10)  # Be friendly to the API
