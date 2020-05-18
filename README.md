# Botnet Detection Engine
A Flow-based Botnet Detection Engine; as a Proof-of-Concept application of a Bio-Optimised Machine Learning Models.

## Getting Started

This is a prototype ML-enabled Flow-based Botnet Detection Engine, with Graphical User Interface, ideally positioned at the Network Edge.

Intended to be ran on a gateway-connected (network edge) switch, with port mirroring enabled (SPAN) to allow the detector PC to collect all network flows.

### Dependencies

Requires ARGUS ... etc

These can be installed with the provided setup script.

### Installing

Clone this repository:
```
git clone github.com/NorthOfNull/BotnetDetectionEngine
```

A setup script is provided in order to check for and install any prerequisites required for program execution:
```
chmod +x setup.sh
./setup.sh
```


## Running the Botnet Detection Engine

A simple bash script is provided in order to run the flow collection and processing programs, which will then feed the flow information to the Botnet Detection Engine script:
```
sudo ./run.sh
```

### Usage
```
usage: botnet_detection_engine.py [-h] [-g] [-l] [-d] [-r READ]

The Botnet Detection Engine. GUI and logging is enabled by default.

optional arguments:
  -h, --help            show this help message and exit
  -g, --no-gui          Disables GUI.
  -l, --no-log          Disables alert and flow logging to file.
  -d, --debug           Enable verbose debugging output.
  -r READ, --read READ  Read from '.pcap' or Network Flow file.
```

### Testing
Includes black and white box unit testing, with testing coverage reports for internal modules.
```
./test.sh
```

