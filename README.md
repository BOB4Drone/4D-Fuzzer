# 4D Fuzzer (a MAVLink fuzzer)


## Description

4D Fuzzer is a fuzzer for fuzzing programs that use MAVLink written in Python.


## Target Program
[PX4-Autopilot Software](https://github.com/PX4/PX4-Autopilot)   
[QGroundControl](https://github.com/mavlink/qgroundcontrol)   
[MAVROS](https://github.com/mavlink/mavros)



## Results

So far the following bugs have been identified:

patched
- [PX4-Autopilot/pull/18371](https://github.com/PX4/PX4-Autopilot/pull/18371)
- [PX4-Autopilot/pull/184114](https://github.com/PX4/PX4-Autopilot/pull/18411)
- [PX4-Autopilot/pull/18655](https://github.com/PX4/PX4-Autopilot/pull/18655)
- [qgroundcontrol/pull/10022](https://github.com/mavlink/qgroundcontrol/pull/10022)
- [qgroundcontrol/pull/10038](https://github.com/mavlink/qgroundcontrol/pull/10038)
- [qgroundcontrol/pull/10062](https://github.com/mavlink/qgroundcontrol/pull/10062)
- [MAVROS/pull/1667](https://github.com/mavlink/mavros/pull/1667)
- [MAVROS/pull/1675](https://github.com/mavlink/mavros/pull/1675)


not patched yet
- [qgroundcontrol/issues/10035](https://github.com/mavlink/qgroundcontrol/issues/10035)
- [qgroundcontrol/issues/10068](https://github.com/mavlink/qgroundcontrol/issues/10068)


## Usage

```
Usage:                [-h, --help] [-m mode] [-i ip] [-p port]
                                      [-I iteration] [-s port]

Optional arguments:                                           
 -h, --help          Show up Options                          
 -m mode             Selcet Target PX4,QGC,MAVROS[default PX4]
 -i ip               Set the Target ip [default 127.0.0.1]    
 -p port             Set the Target port [default 18570]      
 -s port             Use Serial port                          
 -I iteartion per each msgID [default iteration=1]

```
