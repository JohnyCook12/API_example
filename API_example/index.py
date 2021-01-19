

# running simple API

import pyautogui


def main():
    print("hello world")
    pyautogui.typewrite("Hello world 2 from pyautogui")
    pyautogui.press("enter")


if __name__ == "__main__":
    main()