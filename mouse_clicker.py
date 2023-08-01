import pyautogui
import time
import sys


def main():
    user_time = input("Enter click time HH:MM:SS: ")
    hours, minutes, seconds = map(int, user_time.split(':'))

    current_time = time.localtime()
    current_hours, current_minutes, current_seconds = current_time.tm_hour, current_time.tm_min, current_time.tm_sec

    time_diff = (hours - current_hours) * 3600 + (minutes - current_minutes) * 60 + (seconds - current_seconds)
    print(f"Delay is {time_diff} seconds")
    if time_diff < 1:
        print('Wrong time')
        return

    for i in range(0, time_diff):
        sys.stdout.write(f'\rExpected time is {time_diff - i} seconds')
        time.sleep(1)

    current_x, current_y = pyautogui.position()
    pyautogui.click(current_x, current_y)


if __name__ == '__main__':
    main()
