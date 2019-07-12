#!/usr/bin/env python3.7
from enum import Enum, IntEnum
import time


enum = Enum('Menu', 'Pizza Lasagna Spaghetti')
enum3 = IntEnum('Menu', 'Pizza Lasagna Spaghetti')
choice = input("""
        Co zjesz?:
        1. Pizza
        2. Lasagna
        3. Spaghetti
        """)

start = time.perf_counter()

if int(choice) == enum.Pizza.value:
    print("Pizza time!")

if int(choice) == enum3.Pizza:
    print("Pizza time!")

end = time.perf_counter()

time = end - start
print("Time: ", time)