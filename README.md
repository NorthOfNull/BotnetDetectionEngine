# BotnetDetectionEngine
A Flow-based Botnet Detection Engine as a Proof-of-Concept application of a Bio-Optimised Model

## Getting Started

Intended to be ran on a gateway-connected switch, with port mirroring enabled for the detector PC to collect network flows.

### Prerequisites

Requires ARGUS ... etc

### Installing

Clone this repository:

```
git clone github.com/NorthOfNull/BotnetDetectionEngine
```

A setup script is provided in order to check for and install any prerequisites required for program exectuion:

```
./setup
```

## Running the Botnet Detection Engine

A simple bash script is provided in order to run the flow collection and processing programs, which will then feed the flow information to the Botnet Detection Engine script:

 ```
 ./run
 ```
