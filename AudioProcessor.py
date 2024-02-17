"""! @brief The AudioProcessor package.
"""

# @file AudioProcessor.py
#
# @brief This package provides the audio processing functions.
#
# @section description_audioprocessor Description
# This package provides the following audio processing functions:
# - AudioProcessor.audio_generate_sine_wave()
#   - It samples a sine wave sound at a given frequency and amplitude.
# - AudioProcessor.audio_generate_square_wave()
#   - It samples a square wave sound at a given frequency and amplitude.
# - AudioProcessor.audio_generate_sawtooth_wave()
#   - It samples a sawtooth wave sound at a given frequency and amplitude.
# - AudioProcessor.audio_generate_complex_wave()
#   - It samples a complex wave sound at a given frequency and amplitude.
# - AudioProcessor.audio_generate_string_wave()
#   - It samples a string wave sound using the Karplus-Strong algorithm at a given frequency and amplitude.
# - AudioProcessor.audio_note_number_to_freq()
#   - It converts the note number to the corresponding wave frequency.
# - AudioProcessor.audio_stereo_gains()
#   - It compute the left and right channel gains given a stereo pan angle.
# - AudioProcessor.audio_multiply_gain()
#   - It multiplies the input audio data by the input gain.
# - AudioProcessor.audio_rise_fall_envelope()
#   - It applies the rise-fall envelope to the input audio data.
# - AudioProcessor.audio_adsr_envelope()
#   - It applies the ADSR envelope to the input audio data.
# - AudioProcessor.audio_stereo_mix_in()
#   - It mixes a mono channel audio data into the stereo audio data.
#
# @section libraries_audioprocessor Libraries/Modules
# - typing (from the standard library)
#   - access to Tuple
# - math (from the standard library)
#   - access to sqrt, pi, sin, cos, exp, and floor
# - DataStructure
#   - access to DataStructure.Array
#
# @section notes_audioprocessor Notes
# - Comments should be Doxygen compatible.
#
# @section todo_audioprocessor TODO
# Your tasks are to implement the following functions: 
# - AudioProcessor.audio_generate_sine_wave()
# - AudioProcessor.audio_generate_square_wave()
# - AudioProcessor.audio_generate_sawtooth_wave()
# - AudioProcessor.audio_generate_complex_wave()
# - AudioProcessor.audio_generate_string_wave()
# - AudioProcessor.audio_note_number_to_freq()
# - AudioProcessor.audio_stereo_gains()
# - AudioProcessor.audio_multiply_gain()
# - AudioProcessor.audio_rise_fall_envelope()
# - AudioProcessor.audio_adsr_envelope()
# - AudioProcessor.audio_stereo_mix_in()
#
# @section author_audioprocessor Author(s)
# - Created by SingChun Lee on 12/24/2023
# - Modified by SingChun Lee on 12/30/2023
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

from typing import Tuple
from math import sqrt, pi, sin, cos, exp, floor
from DataStructure import Array
## The number of attack samples
adsr_attack_samples = 882
## The number of decay samples
adsr_decay_samples = 882
## The number of release samples
adsr_release_samples = 882

def audio_generate_sine_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int):
    """
    Generates a sine wave based on the specified frequency, amplitude, and sampling rate.

    Parameters:
    - audio_data: Array to store the generated sine wave samples.
    - freq: Frequency of the sine wave in Hz.
    - amp: Amplitude of the sine wave, where 1.0 is maximum amplitude.
    - samples_per_sec: Sampling rate in samples per second (should be 44100 for CD quality).
    """
    for i in range(len(audio_data)):
        t = i / samples_per_sec
        theta = 2 * pi * freq * t
        audio_data[i] = amp * sin(theta)

def audio_generate_square_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int):
    """
    Generates a square wave based on the specified frequency, amplitude, and sampling rate.

    Parameters:
    - audio_data: Array where the generated square wave samples will be stored.
    - freq: The frequency of the square wave in Hz.
    - amp: The amplitude of the square wave. This value should oscillate between -amp and amp.
    - samples_per_sec: The sampling rate in samples per second.
    """
    num_samples = len(audio_data)  # Determine the number of samples based on the audio_data array length

    for i in range(num_samples):
        # Calculate the time in seconds for the current sample
        t = i / samples_per_sec

        # Set the sample value to amp if sin(2pitf) >= 0 , else -amp
        if sin(2*pi*t*freq) >= 0:
            audio_data[i] = amp  # Positive half of the square wave
        else:
            audio_data[i] = -amp  # Negative half of the square wave
        
def audio_generate_sawtooth_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int):
    """
        Generates a sawtooth wave based on the specified frequency, amplitude, and sampling rate.

        Parameters:
        - audio_data: Array where the generated sawtooth wave samples will be stored.
        - freq: The frequency of the sawtooth wave in Hz.
        - amp: The amplitude of the sawtooth wave.
        - samples_per_sec: The sampling rate in samples per second.

        The function modifies the audio_data array in place, filling it with the generated sawtooth wave samples.
        """
    # Iterate through each sample to be generated
    for i in range(len(audio_data)):
        # Calculate the time in seconds for the current sample
        t = i / samples_per_sec
        # Determine how many complete cycles have occurred by this time
        num_cycles = t * freq
        # Calculate the position within the current cycle as a fraction between 0 and 1
        sample_pos = num_cycles - int(num_cycles)  # Keep only the fractional part

        # Calculate the sawtooth wave value for this position in the cycle
        # The formula (2 * sample_pos - 1) maps the range [0,1] to [-1,1]
        # Multiply by amplitude to scale the wave to the desired amplitude
        audio_data[i] = (2 * sample_pos - 1) * amp
          
def sinwave(theta):
    # Implementation of the sinwave function goes here.
    return sin(theta)

def audio_generate_complex_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int):
    # Calculate the number of samples needed
    num_samples = len(audio_data)

    # Create a temporary array to store the complex wave before normalization
    temp_wave = Array(num_samples)

    # Calculate the sinwave values and store them in temp_wave
    for i in range(num_samples):
        t = i / samples_per_sec  # Calculate the time for the current sample
        # Sum of sine waves for different harmonics with exponential decay
        sinwave = sum(sin(2 * j * pi * t * freq) * exp(-0.0008 * pi * t * freq) / 2 ** (j - 1)
                      for j in range(1, 7))
        # Cube the sinwave value and store it in temp_wave
        temp_wave[i] = sinwave ** 3

    # Find the maximum absolute value in the temp_wave for normalization
    max_sinwave = max(abs(sample) for sample in temp_wave)

    # Normalize and store the values in the audio_data array, scaling with the amplitude
    for i in range(num_samples):
        audio_data[i] = (temp_wave[i] / max_sinwave) * amp

def audio_generate_string_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int):
    """
        Generates a string wave using a modified version of the Karplus-Strong algorithm.

        Parameters:
        - audio_data: Array to store the generated string wave samples.
        - freq: The frequency of the note to simulate.
        - amp: The amplitude of the string wave.
        - samples_per_sec: The sampling rate in samples per second.
        """
    # Calculate the size of wave_samples which is based on the desired frequency
    size_wave_samples = int(samples_per_sec / freq)

    # Initialize wave_samples using the audio_generate_square_wave function with an increased frequency
    wave_samples = Array(size_wave_samples)
    audio_generate_square_wave(wave_samples, freq * 100, amp, samples_per_sec)

    # Initialize prev_idx to the last index of the wave_samples
    prev_idx = size_wave_samples - 1
    # Initialize cur_idx to 0
    cur_idx = 0

    # Loop through the audio_data array to fill it with the string wave samples
    for i in range(len(audio_data)):
        # Set the current audio sample to the average of the wave_samples at prev_idx and cur_idx
        audio_data[i] = (wave_samples[prev_idx] + wave_samples[cur_idx]) / 2
        # Set the wave_samples at cur_idx to the new audio_data[i]
        wave_samples[cur_idx] = audio_data[i]
        # Set prev_idx to cur_idx
        prev_idx = cur_idx
        # Advance cur_idx by 1 and wrap it using modulo to stay within the bounds of wave_samples
        cur_idx = (cur_idx + 1) % size_wave_samples

def audio_note_number_to_freq(note_number:int)->float:
    return 440 * (2 ** ((note_number - 69) / 12))

def audio_stereo_gains(angle: float) -> Tuple[float, float]:
    left_gain = (sqrt(2) / 2) * (cos(angle) + sin(angle))
    right_gain = (sqrt(2) / 2) * (cos(angle) - sin(angle))
    return left_gain, right_gain

def audio_multiply_gain(audio_data: Array, gain: float):
    for i in range(len(audio_data)):
        audio_data[i] *= gain

def audio_rise_fall_envelope(audio_data: Array):
    middle_sample_index = len(audio_data) // 2  # Index of the middle sample
    for i in range(len(audio_data)):
        if i <= middle_sample_index:
            gain = i / middle_sample_index
        else:
            gain = (len(audio_data) - 1 - i) / (len(audio_data) - 1 - middle_sample_index)
        audio_data[i] *= gain

def audio_adsr_envelope(audio_data: Array):

    adsr_attack_samples = 882  # Example value for attack samples
    adsr_decay_samples = 882  # Example value for decay samples
    adsr_release_samples = 882  # Example value for release samples
    gain = 1

    if len(audio_data) < adsr_attack_samples + adsr_decay_samples + adsr_release_samples:
        audio_rise_fall_envelope(audio_data)
    else:
        for i in range(len(audio_data)):
            if i < adsr_attack_samples:
                gain = 1.2 * i / adsr_attack_samples
            elif adsr_attack_samples <= i < adsr_attack_samples + adsr_decay_samples:
                gain = 1 + 0.2 * (adsr_attack_samples + adsr_decay_samples - i)/ adsr_decay_samples
            elif adsr_attack_samples + adsr_decay_samples <= i < len(audio_data) - adsr_release_samples:
                gain = 1
            elif len(audio_data) - adsr_release_samples <= i < len(audio_data):
                gain = (len(audio_data) - 1 - i) / adsr_release_samples
            else:
                print("Error")
            audio_data[i] *= gain

def audio_stereo_mix_in(stereo_data: Array, channel_data: Array, which_channel: int):
    if len(stereo_data) != 2 * len(channel_data):
        raise ValueError("Number of stereo audio samples must be twice the number of input channel data")

    for i in range(len(channel_data)):
        if which_channel == 0:  # Left channel
            stereo_data[i * 2] += channel_data[i]
        elif which_channel == 1:  # Right channel
            stereo_data[i * 2 + 1] += channel_data[i]
        else:
            raise ValueError("Invalid channel number. Use 0 for left channel or 1 for right channel")
