import time
import board
import configparser
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import os
import subprocess

MIN_BPM = 30
MAX_BPM = 240
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0

lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.clear()
lcd.color = [100, 0, 0]

config = configparser.ConfigParser()
config_file_path = '/root/scripts/metronome/config.cfg'
config.read(config_file_path)

bmp = config.getint('metronome', 'bmp')
is_metronome_enabled = config.getboolean('metronome', 'is_metronome_enabled')
volume = config.getfloat('metronome', 'volume')
backlight_timeout = config.getint('metronome', 'backlight_timeout')


def turn_off_backlight():
    lcd.color = [0, 0, 0]


def turn_on_backlight():
    lcd.color = [100, 0, 0]


def display_settings():
    enabled = "On" if is_metronome_enabled else "Off"
    lcd.message = f"BPM: {bmp} Vol: {volume:.1f}\nMetronome: {enabled}"


def save_settings():
    config.set('metronome', 'bmp', str(bmp))
    config.set('metronome', 'is_metronome_enabled', str(is_metronome_enabled))
    config.set('metronome', 'volume', str(volume))
    with open(config_file_path, 'w') as configfile:
        config.write(configfile)
    subprocess.run(["sudo", "systemctl", "restart", "metronome.service"])


prev_bmp = bmp - 1
prev_volume = volume - 1
prev_is_metronome_enabled = not is_metronome_enabled


def update_display():
    global prev_bmp, prev_volume, prev_is_metronome_enabled
    bmp_display = f"BPM: {bmp:3}"
    volume_display = f"Vol: {int(volume * 10):2}"
    enabled_display = "On " if is_metronome_enabled else "Off"

    if bmp != prev_bmp:
        lcd.cursor_position(0, 0)  # Move cursor to the beginning of the first row
        lcd.message = bmp_display
        prev_bmp = bmp

    if volume != prev_volume:
        lcd.cursor_position(9, 0)  # Move cursor to the position after BPM display
        lcd.message = volume_display
        prev_volume = volume

    if is_metronome_enabled != prev_is_metronome_enabled:
        lcd.cursor_position(0, 1)  # Move cursor to the beginning of the second row
        lcd.message = f"Metronome: {enabled_display}"
        prev_is_metronome_enabled = is_metronome_enabled

update_display()
last_button_press_time = time.time()
is_backlight_on = True

while True:
    if lcd.right_button or lcd.left_button or lcd.up_button or lcd.down_button or lcd.select_button:
        if not is_backlight_on:
            turn_on_backlight()
            is_backlight_on = True
        last_button_press_time = time.time()  # Update the last button press time

    if lcd.right_button:
        bmp = min(bmp + 1, MAX_BPM)
        update_display()
    elif lcd.left_button:
        bmp = max(bmp - 1, MIN_BPM)
        update_display()
    elif lcd.up_button:
        # Scale the input for internal storage
        volume = min((int(volume * 10) + 1) / 10, MAX_VOLUME)
        update_display()
    elif lcd.down_button:
        # Scale the input for internal storage
        volume = max((int(volume * 10) - 1) / 10, MIN_VOLUME)
        update_display()
    elif lcd.select_button:
        is_metronome_enabled = not is_metronome_enabled
        update_display()
        save_settings()

    if time.time() - last_button_press_time > backlight_timeout and is_backlight_on:
        turn_off_backlight()
        is_backlight_on = False

    time.sleep(0.01)  # Add a small delay to debounce the buttons
