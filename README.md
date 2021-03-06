﻿# Leaf-leaping

This github repository contains information about a project presented at the Raspberry Pi Student Challenge (http://www.illinoistechlex.org/RPstudentindex.html)
Videos of the event can be viewed here:
https://www.youtube.com/watch?v=z5wfaCaQqtU
https://www.youtube.com/watch?v=lpjtA6wt0bg

The project started like any other, with a problem. I love jumping in leaves, but as I grew older, I realized I had less and less time to do it. Whenever I remembered to indulge in this fine fall fun, the results were less than satisfactory. It was too cold, the leaves were damp, or there weren't enough leaves to begin with!

The application uses raspberry pi and python code, and can be broken down into a few sections. Code is modified from already existing code to achieve the goal. It served as a great learning experience to me to see how all the parts fit together!

Camera: The code takes a picture of the ground, then analyzes it pixel-by-pixel to calculate the ratio of "orange:other pixels", or "leaves:not leaves"
Something to note is that the default is rgb, which doesn't tell you what color a pixel is. Instead, convert to hsv and use the hue indicator.

Temperature-humidity sensor: Takes in temperature and humidity, which tells you if it's warm enough to jump in leaves and if the leaves are crisp enough.

WiFi module: Sends an email with picture, leaf concentration, temperature, and humidity to tell you when conditions are optimal for leaf jumping!
