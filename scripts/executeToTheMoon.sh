#!/bin/bash

maxdelay=$((1*60))
delay=$(($RANDOM%maxdelay))
sleep $((delay*60)); 
/usr/bin/python3 /home/mike/Development/raspPiProject/scripts/toTheMoon.py
done