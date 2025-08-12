import tkinter as tk


def window_config(window_width, window_height, compute):
    screen_width = compute.winfo_screenwidth()
    screen_height = compute.winfo_screenheight()

    # Calculate the center coordinates
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    return x, y
