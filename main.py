import argparse
import curses


from visual.start_scene import start_scene
def main(std):
    while True:
        if start_scene(std) == "exit":
            break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Консольная текстовый редактор"
                                                 "на Python.")
    args = parser.parse_args()

    curses.wrapper(main)
