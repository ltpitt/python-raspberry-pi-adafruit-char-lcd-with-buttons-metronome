import daemon
import simpleaudio as sa
import configparser
import os
import time

def set_system_volume(volume):
    # Convert the volume to a percentage (0-100%)
    volume_percentage = max(0, min(int(volume * 100), 100))
    print(volume_percentage)
    os.system(f'amixer sset \'PCM\' {volume_percentage}%')

def run_metronome():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')
    config.read(config_file_path)

    bmp = config.getint('metronome', 'bmp')
    is_metronome_enabled = config.getboolean('metronome', 'is_metronome_enabled')
    audio_file = config.get('metronome', 'audio_file')
    volume = config.getfloat('metronome', 'volume')

    # Set the system volume
    set_system_volume(volume)

    sound_path = os.path.join(os.path.dirname(__file__), 'samples', audio_file)
    print(sound_path)
    wave_obj = sa.WaveObject.from_wave_file(sound_path)

    while True:
        if is_metronome_enabled:
            delay = 60 / bmp
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Wait until the sound has finished playing
            time.sleep(delay)  # No need to adjust for the sound's duration
        else:
            time.sleep(1)  # Sleep for one second if metronome is disabled

if __name__ == "__main__":
    with daemon.DaemonContext():
        run_metronome()