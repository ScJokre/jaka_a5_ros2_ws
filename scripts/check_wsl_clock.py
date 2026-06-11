#!/usr/bin/env python3
"""Detect wall-clock backward jumps that break ROS TF buffers under WSL."""

import argparse
import time


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=20.0)
    args = parser.parse_args()

    end = time.monotonic() + args.seconds
    previous = time.time_ns()
    jumps = []

    print(f"Checking the WSL wall clock for {args.seconds:g} seconds...")
    while time.monotonic() < end:
        current = time.time_ns()
        if current < previous:
            jumps.append((previous - current) / 1_000_000)
            print(f"CLOCK MOVED BACKWARDS by {jumps[-1]:.6f} ms")
        previous = current
        time.sleep(0.001)

    if jumps:
        print(f"FAILED: detected {len(jumps)} backward clock jump(s).")
        return 1

    print("OK: no backward clock jumps detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
