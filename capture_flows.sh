#!/bin/bash

file="output.binetflow"

# Sniff packets using tcpdump, piping output to argus
# Convert to argus data format
# Pass into ra client in order to convert argus data into netflow data
# Then received in the python script, where we can process each flow piped to it's stdin
#( sudo tshark -F pcap -w - | sudo argus -f -r - -w - | ra -r - -c ',' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes | python botnet_detection_engine.py )
( sudo tcpdump -w - | sudo argus -f -r - -w - | ra -r - -c ',' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes | python botnet_detection_engine.py )