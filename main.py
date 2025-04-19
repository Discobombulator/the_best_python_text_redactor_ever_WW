import argparse
import curses

from visual.start_scene import start_scene


def main(std):
    try:
        while True:
            if start_scene(std) == "exit":
                break
    except Exception as e:
        std.addstr(0, 0, f"Fatal error: {str(e)}")
        std.refresh()
        std.getch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Консольная текстовый редактор"
                    "на Python.")
    args = parser.parse_args()

    curses.wrapper(main)
