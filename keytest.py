#!/usr/bin/env python3

import keyboard

while True:
        print(keyboard.read_key() == "unknown")
        # keyboard.on_press_key("r", lambda _:print("You pressed r"))