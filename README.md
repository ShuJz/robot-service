This is a DRL package for robot mp500lwa4d.

Before train the model, pleace determine the default version of Python you are using,

- if it is Python2: you should install gym package in Python2
- if it is Python3: you should install ROS in python3.6 enviroment. For how to install ROS kinetic in python3.6 enviroment, please see the document < Install ROS-Kinetic with Python3.md >



To train the model with a DDPG Agent:

1. Set param ON_TRAIN in script main_distri.py line 19 and RLAgent.py line 12

```python
ON_TRAIN = True
```

2. Then run in bash

```bash
conda activate mp500lwa4d_gym
roslaunch mp500lwa4d_description RL_gazebo_distri.launch
rosrun robot_service RLAgent.py
rosrun robot_service main_distri.py
```

