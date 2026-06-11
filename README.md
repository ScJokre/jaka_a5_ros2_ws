# JAKA A5 ROS 2 MoveIt Demo

This workspace converts the supplied JAKA A5 ROS 1 model into a ROS 2 MoveIt
offline planning demo. It uses `mock_components/GenericSystem`, so **Plan &
Execute only moves the simulated model in RViz**. It does not command a real
JAKA robot.

The original A5 joint geometry, limits, and STL meshes came from:

`机械臂相关资料JAKA-A5+UR5e/JAKA_A5_Docs/ROS V2.2/jaka_robot_v2.2/src`

## WSL prerequisites

This configuration targets Ubuntu 24.04 with ROS 2 Jazzy, matching the tested
WSL environment. MoveIt 2 Humble uses an older OMPL parameter format and needs
a separate `ompl_planning.yaml`.

```bash
source /opt/ros/$ROS_DISTRO/setup.bash
sudo apt update
sudo apt install \
  ros-$ROS_DISTRO-moveit \
  ros-$ROS_DISTRO-ros2-control \
  ros-$ROS_DISTRO-ros2-controllers \
  ros-$ROS_DISTRO-xacro \
  python3-colcon-common-extensions \
  python3-rosdep
```

WSL2 with WSLg should display RViz directly. Confirm `echo $DISPLAY` is not
empty before launching.

## Build

After transferring `jaka_a5_ros2_ws` into WSL:

```bash
cd ~/jaka_a5_ros2_ws
source /opt/ros/$ROS_DISTRO/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run the Panda-style planning test

```bash
ros2 launch jaka_a5_moveit_config demo.launch.py
```

In RViz:

1. Open the **MotionPlanning** panel.
2. Set **Planning Group** to `jaka_a5` if it is not already selected.
3. In **Planning**, choose `ready` as the start state or use the current state.
4. Drag the orange/blue interactive marker at `tool0`, or choose `zero`/`ready`
   as a goal state.
5. Click **Plan** first. If the result is valid, click **Execute**, or use
   **Plan & Execute**.

The terminal should show these active controllers:

```bash
ros2 control list_controllers
```

Expected output includes:

```text
jaka_a5_controller      joint_trajectory_controller/JointTrajectoryController active
joint_state_broadcaster joint_state_broadcaster/JointStateBroadcaster         active
```

## Basic troubleshooting

If RViz opens but no robot appears:

```bash
ros2 topic echo /joint_states --once
ros2 topic echo /robot_description --once
ros2 run tf2_ros tf2_echo world tool0
```

If mesh loading fails, verify the description package is discoverable:

```bash
ros2 pkg prefix jaka_a5_description
```

If planning is slow, the supplied STL files are being used directly for
collision checking. Generate simpler collision meshes later; do not reduce the
visual meshes.

If `mock_components/GenericSystem` is missing:

```bash
sudo apt install ros-$ROS_DISTRO-ros2-control ros-$ROS_DISTRO-ros2-controllers
```

If the terminal repeatedly prints `TF_OLD_DATA` or `Moved backwards in time`,
the WSL clock has jumped backwards. Stop the launch, run `wsl --shutdown` from
Windows PowerShell, reopen WSL, and launch again.

## Important limitations

- This configuration has not been connected to a real JAKA controller.
- Joint limits are based on the supplied JAKA ROS V2.2 files. Verify them
  against the exact physical robot before commanding hardware.
- `tool0` is currently fixed at the supplied `J6` frame origin. Measure and
  update `tool0_fixed` when mounting a gripper or other tool.
- The source package's self-collision exclusions were retained. Re-run the
  MoveIt Setup Assistant collision matrix if the mechanical setup changes.
