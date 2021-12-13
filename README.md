
# 4D Fuzzer (a MAVLink fuzzer)


## Description

4D Fuzzer is a fuzzer for fuzzing programs that use MAVLink written in Python3.


## Quick Start
만약 PX4 시뮬레이터를 대상으로 테스팅을 수행하려면 다음과 같이 실행하세요.
```
python3 4dfuzzer.py
```
시리얼 통신을 이용해 퍼징을 할 경우 이렇게 실행하세요.
```
python3 4dfuzzer.py -s [port]
```
각 msgid별  iteration을 설정하고 싶다면 이렇게 실행하세요.
```
python3 4dfuzzer.py -I [iteration]
```

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
