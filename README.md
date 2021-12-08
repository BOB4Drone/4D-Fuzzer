# 4D Fuzzer (mavlink fuzzer)

## Description

This is an effort to test the MAVLink works written in python using fuzz testing.

## Target Program
[PX4-Autopilot Software](https://github.com/PX4/PX4-Autopilot)
[QGroundControl Ground Control Station](https://github.com/mavlink/qgroundcontrol)
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

not patched yet
- [qgroundcontrol/issues/10035](https://github.com/mavlink/qgroundcontrol/issues/10035)
- [mavros/issues/1668](https://github.com/mavlink/mavros/issues/1668)
- [qgroundcontrol/issues/10068](https://github.com/mavlink/qgroundcontrol/issues/10068)

## Dependency


## Using 4D Fuzzer
```
  -i dir        - input directory with test cases
  -o dir        - output directory for fuzzer findings
```
