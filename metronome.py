import daemon
import simpleaudio as sa
import configparser
import os
import time
import threading


def set_system_volume(volume):
    volume_percentage = max(0, min(int(volume * 100), 100))
    print(volume_percentage)
    os.system(f'amixer sset \'PCM\' {volume_percentage}%')


def play_tick(sound_path):
    while True:
        wave_obj = sa.WaveObject.from_wave_file(sound_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()


def run_metronome():
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.cfg')
    config.read(config_file_path)
    bpm = config.getint('metronome', 'bpm')
    is_metronome_enabled = config.getboolean('metronome', 'is_metronome_enabled')
    audio_file = config.get('metronome', 'audio_file')
    volume = config.getfloat('metronome', 'volume')

    # Set the system volume
    set_system_volume(volume)

    sound_path = os.path.join(os.path.dirname(__file__), 'samples', audio_file)
    print(sound_path)

    delay = 60 / bpm
    while True:
        if is_metronome_enabled:
            print(f"Ticking at {bpm} BPM")
            threading.Thread(target=play_tick, args=(sound_path,)).start()
            time.sleep(delay)
        else:
            time.sleep(1)


if __name__ == "__main__":
    with daemon.DaemonContext():
        run_metronome()
