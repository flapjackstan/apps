"""Simple timer app with sounds notifications."""

import argparse
import os
import time

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame


def parse_time(time_str: str) -> int:
    """Convert a time string of format MM:SS to total seconds."""
    minutes, seconds = map(int, time_str.split(":"))
    return minutes * 60 + seconds


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    p = argparse.ArgumentParser(
        description=__doc__, usage="python timer.py --total 1:00 --sub 0:30 1:00 1:15"
    )
    p.add_argument(
        "--total",
        type=str,
        required=True,
        help="Total time in minutes:seconds for the final timer",
    )
    p.add_argument(
        "--sub",
        type=str,
        required=False,
        nargs="+",
        help="Space separated time intervals in minutes:seconds for timer to notify you at",
    )
    return p.parse_args()


def play_sound(file_path: str) -> None:
    """Play a sound file."""
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)


def start_timers(args: argparse.Namespace) -> None:
    """
    Run timers for the total time and subtimers if provided.

    Print notifications are sent to terminal at the end of each timer. All subtimers must occur before the final timer
    """
    print(f"Time Started at {time.strftime('%H:%M:%S', time.localtime(time.time()))}")
    total_seconds = parse_time(args.total)
    subtimers = sorted([parse_time(sub) for sub in args.sub]) if args.sub else []

    start_time = time.time()
    sub_index = 0

    while True:
        elapsed_time = time.time() - start_time

        if sub_index < len(subtimers) and elapsed_time >= subtimers[sub_index]:
            minutes, seconds = divmod(subtimers[sub_index], 60)
            print(
                f"Subtimer {minutes} minute(s) and {seconds} second(s) elapsed "
                f"at {time.strftime('%H:%M:%S', time.localtime(time.time()))}!"
            )
            play_sound("/Users/elmer/Documents/dev/apps/assets/notification.mp3")
            sub_index += 1

        if elapsed_time >= total_seconds:
            minutes, seconds = divmod(total_seconds, 60)
            print(
                f"Total time {minutes} minute(s) and {seconds} second(s) elapsed "
                f"at {time.strftime('%H:%M:%S', time.localtime(time.time()))}!"
            )
            play_sound("/Users/elmer/Documents/dev/apps/assets/notification.mp3")
            break

        time.sleep(1)


def main():
    """Run script as an app."""
    args = parse_args()
    start_timers(args)


if __name__ == "__main__":
    main()
