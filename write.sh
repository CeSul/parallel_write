#!/bin/bash

ffmpeg -i "output/plot%05d.png" -c:v libx264 -pix_fmt yuv420p melt.mp4
