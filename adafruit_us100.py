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

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_US100.git"

class US100:
    """Control a US-100 ultrasonic range sensor."""

    def __init__(self, uart):
        self._uart = uart

    @property
    def distance(self):
        """Return the distance measured by the sensor in cm.
        This is the function that will be called most often in user code.
        If no signal is received, we'll throw a RuntimeError exception. This means
        either the sensor was moving too fast to be pointing in the right
        direction to pick up the ultrasonic signal when it bounced back (less
        likely), or the object off of which the signal bounced is too far away
        for the sensor to handle. In my experience, the sensor can detect
        objects over 460 cm away.
        :return: Distance in centimeters.
        :rtype: float
        """
        self._uart.write(bytes([0x55]))
        data = self._uart.read(2)  # 2 bytes return for distance
        if len(data) != 2:
            raise RuntimeError("Did not receive distance response")
        dist = (data[1] + (data[0] << 8)) / 10
        return dist

    @property
    def temperature(self):
        """Return the on-chip temperature, in Celsius"""
        self._uart.write(bytes([0x50]))
        data = self._uart.read(1)  # 1 byte return for temp
        if len(data) != 1:
            raise RuntimeError("Did not receive temperature response")
        temp = data[0] - 45
        return temp
