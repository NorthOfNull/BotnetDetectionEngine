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
./setup.sh
```


## Running the Botnet Detection Engine

A simple bash script is provided in order to run the flow collection and processing programs, which will then feed the flow information to the Botnet Detection Engine script:
```
./run.sh
```

### Usage
```
usage: ./run.sh [-h --help] [-n] [--log] 

The Botnet Detection Engine. GUI starts by default. Logging is disabled by
deafult (to stdout only).

optional arguments:
	
   -h, --help  show this help message and exit
  
  -n          Disables GUI.
  --log       Log output to
              "/var/log/botnet_detection_engine/detection_output.log".
```
