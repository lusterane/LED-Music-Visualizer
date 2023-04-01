import argparse
from src.stream_analyzer import Stream_Analyzer
from src.color_mapper import Color_Mapper
from src.color_mapper import Color_Theme
from src.serial_data_manager import Serial_Data_Manager
import time
from enum import Enum

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=None, dest='device',
                        help='pyaudio (portaudio) device index')
    parser.add_argument('--height', type=int, default=450, dest='height',
                        help='height, in pixels, of the visualizer window')
    parser.add_argument('--n_frequency_bins', type=int, default=400, dest='frequency_bins',
                        help='The FFT features are grouped in bins')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--window_ratio', default='24/9', dest='window_ratio',
                        help='float ratio of the visualizer window. e.g. 24/9')
    parser.add_argument('--sleep_between_frames', dest='sleep_between_frames', action='store_true',
                        help='when true process sleeps between frames to reduce CPU usage (recommended for low update rates)')
    return parser.parse_args()

def convert_window_ratio(window_ratio):
    if '/' in window_ratio:
        dividend, divisor = window_ratio.split('/')
        try:
            float_ratio = float(dividend) / float(divisor)
        except:
            raise ValueError('window_ratio should be in the format: float/float')
        return float_ratio
    raise ValueError('window_ratio should be in the format: float/float')

def run_FFT_analyzer():
    args = parse_args()
    window_ratio = convert_window_ratio(args.window_ratio)

    ear = Stream_Analyzer(
                    device = args.device,        # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = None,               # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 60,    # Window size used for the FFT transform
                    updates_per_second  = 1000,  # How often to read the audio stream for new data
                    smoothing_length_ms = 50,    # Apply some temporal smoothing to reduce noisy features
                    n_frequency_bins = args.frequency_bins, # The FFT features are grouped in bins
                    visualize = 1,               # Visualize the FFT features with PyGame
                    verbose   = args.verbose,    # Print running statistics (latency, fps, ...)
                    height    = args.height,     # Height, in pixels, of the visualizer window,
                    window_ratio = window_ratio  # Float ratio of the visualizer window. e.g. 24/9
                    )

    color_mapper = Color_Mapper(Color_Theme.MOUNTAIN_DEW.value)
    serial_manager = Serial_Data_Manager()

    fps = 30  #How often to update the FFT features + display
    last_update = time.time()

    while True:
        if (time.time() - last_update) > (1./fps):
            last_update = time.time()
            raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()

            # process rgb value
            if color_mapper.update_frequencies(ear.frequency_bin_energies):
                power = convert_255_scale(color_mapper.get_power())
                color = color_mapper.get_color()
                ret_str = serial_manager.create_data_string(Lighting_Preset.MOVING_WAVES.value, color, power)
                # print_power(power)
                serial_manager.write(ret_str)

        elif args.sleep_between_frames:
            time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)
def convert_255_scale(power):
    power *= 100
    power = int(power)
    # scale to 255
    power = 255 * power // 100
    if power >= 251:
        power = 250
    return power
def print_power(power):
    # convert to 100 scale
    power = (power / 255) * 100
    for _ in range(int(power)):
        print('.',end='')
    for _ in range(100-int(power)):
        print(' ',end='')
    print('|')

class Lighting_Preset(Enum):
    MOVING_WAVES = "0"
    ALL_LIGHTS = "1"
    EXPAND_FROM_MIDDLE = "2"


def test_arduino():
    # serial_manager = Serial_Data_Manager()
    # res = serial_manager.write_test()
    import serial
    s = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
    time.sleep(2)
    while True:
        s.write('0\n'.encode())
        print("giving 0")
        time.sleep(1)


        s.write('58\n'.encode())
        print('giving 58')
        time.sleep(1)


    # while True:
    # time.sleep(2)
    # print(s.readline())


if __name__ == '__main__':
    run_FFT_analyzer()
    # test_arduino()