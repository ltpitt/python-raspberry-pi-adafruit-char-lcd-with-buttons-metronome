# Raspberry Pi Metronome with LCD and Buttons

This project turns your Raspberry Pi into a fully functional metronome, complete with an interactive LCD display and button controls. It's perfect for musicians who need a reliable and customizable tempo guide during practice sessions.

## Features

- Adjustable BPM: Set the beats per minute (BPM) to your desired tempo.
- Audio Feedback: Hear the metronome beats through a connected speaker.
- LCD Display: View current settings on a 16x2 character LCD.
- Button Controls: Easily adjust BPM and volume, and toggle the metronome on/off.
- Auto-Save: Settings are saved automatically and persist between sessions.
- Backlight Timeout: The LCD backlight turns off after a period of inactivity to save power.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Adafruit 16x2 Character LCD + Keypad for Raspberry Pi
- Speakers or headphones for audio output

## Software Setup

1. Clone the repository to your Raspberry Pi:  
   ```git clone https://github.com/ltpitt/python-raspberry-pi-adafruit-char-lcd-with-buttons-metronome.git```

2. Navigate to the cloned directory:  
   ```cd python-raspberry-pi-adafruit-char-lcd-with-buttons-metronome```

3. Create a virtual environment and activate it:  
   ```python3 -m venv venv```
   ```source venv/bin/activate```

4. Install the required dependencies:  
   ```pip install -r requirements.txt```

## Configuration

Customize the config.cfg file to set the initial BPM, volume, and backlight timeout:

```
[metronome]
bmp = 90
is_metronome_enabled = False
audio_file = metronome_classic_1.wav
volume = 0.7
backlight_timeout = 30
```

## Running the Metronome

To start the metronome, use the provided systemd service files.

## Important Note on Service Files

Before enabling and starting the services, ensure that the paths specified in the `ExecStart` lines of both `metronome.service` and `metronome_lcd.service` match the location where you have cloned the repository. If your repository is located in a different folder, update the paths accordingly.

For example, if your cloned repository is in `/home/pi/metronome`, the `ExecStart` line should be:  
```ExecStart=/home/pi/metronome/venv/bin/python /home/pi/metronome/metronome.py```

Make these changes in both service files before proceeding with the service setup.


1. Copy the service files to /etc/systemd/system/:  
   ```sudo cp metronome.service /etc/systemd/system/```
   ```sudo cp metronome_lcd.service /etc/systemd/system/```

2. Enable and start the services:  
   ```sudo systemctl enable metronome.service```
   ```sudo systemctl start metronome.service```
   ```sudo systemctl enable metronome_lcd.service```
   ```sudo systemctl start metronome_lcd.service```

The metronome will now start automatically on boot.

## Usage

- Right Button: Increase BPM.
- Left Button: Decrease BPM.
- Up Button: Increase volume.
- Down Button: Decrease volume.
- Select Button: Toggle the metronome on/off.

The LCD will display the current BPM, volume level, and whether the metronome is active.

## Contributing

Contributions to this project are welcome! Please feel free to submit issues, pull requests, or suggestions to improve the metronome.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
