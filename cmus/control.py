#!/usr/bin/env python3
"""
Volume key monitor for Beepy.
Listens for volume up/down key presses on the keyboard device
and calls cmus_remote to adjust media volume.

Usage:
    python3 main.py [--device /dev/input/event4] [--step 0.05]

Requirements:
    - cmus_remote (for controlling MPRIS players)
    - Read access to the input device (run as root or add user to 'input' group)
"""

import argparse
import fcntl
import logging
import os
import re
import struct
import subprocess
import sys
import time
import threading

# Linux input event constants (from linux/input-event-codes.h)
EV_KEY = 0x01

# Key codes
KEY_VOLUMEUP = 115
KEY_VOLUMEDOWN = 114
KEY_PLAYPAUSE = 164
pauseCount=0
clickInterval=0.5

# struct input_event: timeval (2x long) + type, code, value (3x int)
# On 64-bit: long long (8 bytes) x2 for time, then int x3
# On 32-bit (arm): long (4 bytes) x2 for time, then int x3
import platform

if platform.architecture()[0] == "64bit":
    INPUT_EVENT_FORMAT = "llHHI"
    INPUT_EVENT_SIZE = struct.calcsize(INPUT_EVENT_FORMAT)
else:
    INPUT_EVENT_FORMAT = "iiHHI"
    INPUT_EVENT_SIZE = struct.calcsize(INPUT_EVENT_FORMAT)


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def run_cmus_remote(args: list[str]) -> bool:
    """Run cmus_remote with the given args. Returns True on success."""
    print(args)
    try:
        result = subprocess.run(
            ["cmus-remote","--server","/run/user/1000/cmus-socket", *args],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            logging.warning("cmus_remote %s failed: %s", " ".join(args), result.stderr.strip())
            return False
        logging.debug("cmus_remote %s -> %s", " ".join(args), result.stdout.strip())
        return True
    except FileNotFoundError:
        logging.error("cmus_remote not found. Install with: sudo apt install cmus_remote")
        return False
    except subprocess.TimeoutExpired:
        logging.warning("cmus_remote %s timed out", " ".join(args))
        return False

def adjust_volume(direction: str, step: float) -> None:
    """Adjust volume up or down using cmus-remote."""
    if direction == "up":
        run_cmus_remote(["-v", f"+{step:g}%"])
    elif direction == "down":
        run_cmus_remote(["-v", f"-{step:g}%"])

def open_device(path: str):
    """Open the input device file."""
    found=False
    while not found:
        try:
            fd = os.open(path, os.O_RDONLY)
            found=True
        except PermissionError:
            logging.error(
            "Permission denied opening %s. Run as root or: "
            "sudo usermod -a -G input $USER",
            path,
            )
            sys.exit(1)
        except FileNotFoundError:
            time.sleep(1)
    return fd


def grab_device(fd: int) -> None:
    """Optionally grab the device so key events don't go to other consumers."""
    EVIOCGRAB = 0x40044590
    try:
        fcntl.ioctl(fd, EVIOCGRAB, 1)
        logging.debug("Device grabbed (exclusive access).")
    except OSError as e:
        logging.warning("Could not grab device: %s", e)
def timer_callback():
    global pauseCount
    if pauseCount==1:
        run_cmus_remote(["-u"])
    elif pauseCount==2:
        run_cmus_remote(["-n"])
    pauseCount=0




def main() -> None:
    parser = argparse.ArgumentParser(description="Volume key monitor using cmus-remote")
    parser.add_argument(
        "--device",
        #default="/dev/input/event1",
        default="/dev/input/by-id/usb-TTGK_Technology_Co._Ltd_CX31993_384Khz_HIFI_AUDIO-event-if03",
        help="Input device to monitor (default: /dev/input/event4 = beepy-kbd)",
    )
    parser.add_argument(
        "--step",
        type=float,
        default=5,
        help="Volume step as fraction (default: 0.05 = 5%%)",
    )
    parser.add_argument(
        "--grab",
        action="store_true",
        help="Grab the device exclusively (recommended if other apps also read it)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()
    setup_logging(args.verbose)
    fd = open_device(args.device)
    if args.grab:
        grab_device(fd)
    logging.info("Monitoring %s for volume keys (step: %.0f%%)...", args.device, args.step * 100)
    try:
        while True:
            # Read raw input events (blocking read of one struct)
            try:
                data = os.read(fd, INPUT_EVENT_SIZE)
            except OSError:
                fd = open_device(args.device)
                continue

            if len(data) < INPUT_EVENT_SIZE:
                continue

            _, _, ev_type, code, value = struct.unpack(INPUT_EVENT_FORMAT, data)

            # Only act on key press (value == 1, not release=0 or repeat=2)
            if ev_type != EV_KEY or value != 1:
                continue

            global pauseCount
            if code == KEY_VOLUMEUP:
                adjust_volume("up", args.step)
            elif code == KEY_VOLUMEDOWN:
                adjust_volume("down", args.step)
            elif code == KEY_PLAYPAUSE:
                if pauseCount==0:
                    timer=threading.Timer(clickInterval,timer_callback)
                    timer.start()
                    pauseCount=1
                elif pauseCount==1:
                    if timer.is_alive():
                        timer.cancel()
                        pauseCount=2
                        timer=threading.Timer(clickInterval,timer_callback)
                        timer.start()
                elif pauseCount==2:
                    if timer.is_alive():
                        timer.cancel()
                        pauseCount=0
                        run_cmus_remote(["-r"])

    except KeyboardInterrupt:
        logging.info("Stopped.")
    finally:
        os.close(fd)

if __name__ == "__main__":
    main()
