# The MIT License (MIT)
#
# Copyright (c) 2018 ladyada for adafruit industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_us100`
====================================================

CircuitPython library for reading distance and temperature via US-100 ultra-sonic sensor

* Author(s): ladyada

Implementation Notes
--------------------


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_US100.git"

import time


class US100:
    """Control a US-100 ultrasonic range sensor."""

    def __init__(self, uart):
        self._uart = uart

    @property
    def distance(self):
        """Return the distance measured by the sensor in cm.
        This is the function that will be called most often in user code.
        If no signal is received, return ``None``. This can happen when the
        object in front of the sensor is too close, the wiring is incorrect or the
        sensor is not found. If the signal received is not 2 bytes, return ``None``.
        This means either the sensor was moving too fast to be pointing in the right
        direction to pick up the ultrasonic signal when it bounced back (less
        likely), or the object off of which the signal bounced is too far away
        for the sensor to handle. In my experience, the sensor can not detect
        objects over 460 cm away.
        :return: Distance in centimeters.
        :rtype: float
        """
        for _ in range(2):  # Attempt to read twice.
            self._uart.write(bytes([0x55]))
            time.sleep(0.1)
            data = self._uart.read(2)  # 2 byte return for distance.
            if data:  # If there is a reading, exit the loop.
                break
            time.sleep(0.1)  # You need to wait between readings, so delay is included.
        else:
            # Loop exited normally, so read failed twice.
            # This can happen when the object in front of the sensor is too close, if the wiring
            # is incorrect or the sensor is not found.
            return None

        if len(data) != 2:
            return None

        dist = (data[1] + (data[0] << 8)) / 10
        return dist

    @property
    def temperature(self):
        """Return the on-chip temperature, in Celsius"""
        for _ in range(2):  # Attempt to read twice.
            self._uart.write(bytes([0x50]))
            time.sleep(0.1)
            data = self._uart.read(1)  # 1 byte return for temp
            if data:  # If there is a reading, exit the loop.
                break
            time.sleep(0.1)  # You need to wait between readings, so delay is included.
        else:
            # Loop exited normally, so read failed twice.
            # This can happen when the object in front of the sensor is too close, if the wiring
            # is incorrect or the sensor is not found.
            return None

        if len(data) != 1:
            return None

        temp = data[0] - 45
        return temp
