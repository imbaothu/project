"""! @brief The AudioProcessor package.
"""

##
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

def audio_generate_sine_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int) -> None:
    """! This function generates a sine wave audio data.
    
    Given an input frequency **freq** and an amplitude **amp**, this function samples the continuous sine function \f(\sin\f) to the input Array **audio_data**. The sampling rate is determined by the input samples per second **samples_per_sec**. For each sample in **audio_data** (denote it as the **i**-th sample), this function first computes the current time **t** (dividing **i** by **samples_per_sec**). Then, it computes the current angle **theta** (multiplying **t** by **freq** and \f(2\pi\f)). At last, it sets the **i**-th sample **audio_data[i]** to \f(\sin\f)(**theta**) * **amp**.
    
    @param audio_data The audio data.
    
    @param freq The sine wave frequency.
    
    @param amp The sine wave amplitude.
    
    @param samples_per_sec The number of samples per second.
    """
    for i in range(len(audio_data)):
        t = i / samples_per_sec
        audio_data[i] = amp * sin(2 * pi * freq * t)

    
    

def audio_generate_square_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int) -> None:
    """! This function generates a square wave audio data.
    
    Given an input frequency **freq** and an amplitude **amp**, this function samples the continuous square function \f(\mathrm{square}\f) to the input Array **audio_data**. The sampling rate is determined by the input samples per second **samples_per_sec**. For each sample in **audio_data** (denote it as the **i**-th sample), this function first computes the current time **t** (dividing **i** by **samples_per_sec**). Then, it computes the current angle **theta** (multiplying **t** by **freq** and \f(2\pi\f)). At last, it sets the **i**-th sample **audio_data[i]** to \f(\mathrm{square}\f)(**theta**) * **amp**. Note that, one can compute \f(\mathrm{square}\f)(**theta**) using \f(\sin\f)(**theta**) as follows:
        \f(
        \mathrm{square}(\theta) = \begin{cases}
            1 & \text{if } \sin(\theta) \geq 0 \\
            -1 & \text{otherwise.}
        \end{cases}
        \f)
    
    @param audio_data The audio data.
    
    @param freq The square wave frequency.
    
    @param amp The square wave amplitude.
    
    @param samples_per_sec The number of samples per second.
    """
    for i in range(len(audio_data)):
        t = i / samples_per_sec
        audio_data[i] = amp if sin(2 * pi * freq * t) >= 0 else -amp

def audio_generate_sawtooth_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int) -> None:
    """! This function generates a sawtooth wave audio data.
    
    Given an input frequency **freq** and an amplitude **amp**, this function samples the continuous sawtooth function \f(\mathrm{sawtooth}\f) to the input Array **audio_data**. The sampling rate is determined by the input samples per second **samples_per_sec**. For each sample in **audio_data** (denote it as the **i**-th sample), this function first computes the current time **t** (dividing **i** by **samples_per_sec**). Then, it computes the current cycle **num_cycles** (multiplying **t** by **freq**) and the current sampling position **sample_pos** (the decimal part of **num_cycles**). At last, it sets the **i**-th sample **audio_data[i]** to \f(\mathrm{sawtooth}\f)(**sample_pos**) * **amp**. Note that, one can compute \f(\mathrm{sawtooth}\f)(**sample_pos**) as follows:
        \f(
        \mathrm{sawtooth}(p) = -1 + 2p
        \f)
    
    @param audio_data The audio data.
    
    @param freq The sawtooth wave frequency.
    
    @param amp The sawtooth wave amplitude.
    
    @param samples_per_sec The number of samples per second.
    """
    
    for i in range(len(audio_data)):
        t = i / samples_per_sec
        sample_pos = (t * freq) - floor(t * freq)
        audio_data[i] = amp * (-1 + 2 * sample_pos)

def audio_generate_complex_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int) -> None:
    """! This function generates a complex wave audio data.
    
    Given an input frequency **freq** and an amplitude **amp**, this function samples the continuous complex sine wave function \f(\mathrm{complex}\f) to the input Array **audio_data**. The sampling rate is determined by the input samples per second **samples_per_sec**. For each sample in **audio_data** (denote it as the **i**-th sample), this function first computes the current time **t** (dividing **i** by **samples_per_sec**). Then, it computes the current angle **theta** (multiplying **t** by **freq** and \f(2\pi\f)). At last, it sets the **i**-th sample **audio_data[i]** to \f(\mathrm{complex}\f)(**theta**) * **amp**. In this project, we define the \f(\mathrm{complex}\f)(**theta**) using \f(\mathrm{\sin}\f)(**theta**) as follows:
        \f(
        \mathrm{complex}(\theta) = \frac{\mathrm{sinwave}(\theta)}{\max(|\mathrm{sinwave}|)}
        \f)
    where \f(\mathrm{sinwave}\f)(**theta**) is defined as:
        \f(
        \mathrm{sinwave}(\theta) = \left( (\sin(\theta) + \frac{1}{2}\sin(2\theta) + \frac{1}{4}\sin(3\theta) + \frac{1}{8}\sin(4\theta) + \frac{1}{16}\sin(5\theta) + \frac{1}{32}\sin(6\theta)) \times \exp(-0.0004\theta)\right)^3
        \f)
    and \f(\max(|\mathrm{sinwave}|)\f) is the maximum of the absolute value of all \f(\mathrm{sinwave}(\theta)\f).
    
    @param audio_data The audio data.
    
    @param freq The complex wave frequency.
    
    @param amp The complex wave amplitude.
    
    @param samples_per_sec The number of samples per second.
    """
    
    def sinwave(theta: float) -> float:
        components = sum((1/2**i) * sin((i+1) * theta) for i in range(6))
        decay = exp(-0.0004 * theta)
        return (components * decay) ** 3

    max_sinwave = max(abs(sinwave(2 * pi * freq * t / samples_per_sec)) for t in range(samples_per_sec))
    
    for i in range(len(audio_data)):
        t = i / samples_per_sec
        theta = 2 * pi * freq * t
        audio_data[i] = amp * (sinwave(theta) / max_sinwave)

def audio_generate_string_wave(audio_data: Array, freq: float, amp: float, samples_per_sec: int) -> None:
    """! This function generates a string wave audio data.
    
    Given an input frequency **freq** and an amplitude **amp**, this function samples the continuous string function \f(\mathrm{string}\f), using the Karplus-Strong algorithm (https://en.wikipedia.org/wiki/Karplus%E2%80%93Strong_string_synthesis), to the input Array **audio_data**. The sampling rate is determined by the input samples per second **samples_per_sec**. In a word, the Karplus-Strong algorithm continuously and repeatedly averages consecutive random wave samples into the output string samples. In this project, this function implements a modified version of the Karplus-Strong algorithm as follows:
    
    - First, instead of using random samples, the function initializes an Array **wave_samples** of size **samples_per_sec** / **freq**, and calls audio_generate_square_wave() to create **wave_samples**.
    - Then, initialize **prev_idx** to the last index of the wave samples and **cur_idx** to 0.
    - For each sample in **audio_data** (denote it as the **i**-th sample), 
      - set the current audio sample (**audio_data[i]**) to the average of the wave samples (**wave_samples**) at **prev_idx** and **cur_idx**.
      - set the wave samples at **cur_idx** to **audio_data[i]**.
      - set **prev_idx** to **cur_idx**.
      - advance **cur_idx** by 1. If it is out of bounds, reset it to 0. Hint: You may handle the out-of-bound situation by using the modulo operator.
    
    @param audio_data The audio data.
    
    @param freq The string wave frequency.
    
    @param amp The string wave amplitude.
    
    @param samples_per_sec The number of samples per second.
    """
    
    size = int(samples_per_sec / freq)
    wave_samples = [0.0] * size
    
    audio_generate_square_wave(wave_samples, freq, amp, samples_per_sec)
    
    prev_idx = size - 1
    curIdx = 0
    
    for i in range(len(audio_data)):
        audio_data[i] = (wave_samples[prev_idx] + wave_samples[curIdx]) / 2
        
        wave_samples[curIdx] = audio_data[i]
        
        prev_idx = curIdx
        curIdx = (curIdx + 1) % size


def audio_note_number_to_freq(note_number: int) -> float:
    """! This function converts the song note number to wave frequency.
    
    Musical note numbers can be converted to their corresponding wave frequencies (Ref: https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies). In short, given a note number **note_number** (denote by \f(n\f)), this function returns the corresponding wave frequency using this formula: \f(440 \times 2^{\frac{n - 69}{12}}\f).
    
    @param note_number The input note number.
    
    @return The converted wave frequency.
    """
    
    pass



def audio_stereo_gains(angle: float) -> Tuple[float, float]:
    """! This function takes the angle between two stereo sources, computes and returns the two channel gains.
    
    This function computes appropriate gains for the stereo left and right channels, according to a pan angle **angle** specified in radians. It returns a tuple of two gains using the below formula. Given an angle \f(\theta\f), the left \f(L\f) and right \f(R\f) gains are: \f(L = \frac{\sqrt{2}}{2} (\cos(\theta) + \sin(\theta))\f) and \f(R = \frac{\sqrt{2}}{2} (\cos(\theta) - \sin(\theta))\f).
    
    @param angle The pan angle between the two stereo sources.
    
    @return A tuple of the left and right channel gains.
    """
    # Using half the square root of two as a multiplier for both channels
    root_two_half = sqrt(2) / 2
    # Compute the left and right gains using trigonometric functions
    gain_left = root_two_half * (cos(angle) + sin(angle))
    gain_right = root_two_half * (cos(angle) - sin(angle))
    
    return gain_left, gain_right


    
    


def audio_multiply_gain(audio_data: Array, gain: float) -> None:
    """! This function multiplies the audio data by the input gain.
    
    This function multiples the input Array **audio_data** by the input **gain**. For each sample in **audio_data**, it is multiplied by **gain**.
    
    @param audio_data The audio data.
    @param gain The input gain.
    """
    for i in range(len(audio_data)):
        audio_data[i] *= gain

    
    

def audio_rise_fall_envelope(audio_data: Array) -> None:
      """Apply a simple rise/fall envelope to the audio data."""
      m = len(audio_data) // 2
      for i in range(len(audio_data)):
        if i <= m:  # Rise phase
            gain = i / m
        else:  # Fall phase
            gain = (len(audio_data) - 1 - i) / (len(audio_data) - 1 - m)
        audio_data[i] *= gain


def audio_adsr_envelope(audio_data: Array) -> None:
    """Applies the ADSR envelope to the input audio data.

    Args:
        audio_data: The audio data as an Array of floats.
    """
    total_length = len(audio_data)  # This requires your Array class to support len()
    
    total_adsr_samples = adsr_attack_samples + adsr_decay_samples + adsr_release_samples

    if total_length < total_adsr_samples:
        # If not enough samples for ADSR, apply rise/fall envelope
        audio_rise_fall_envelope(audio_data)
        return

    for i in range(total_length):
        if i < adsr_attack_samples:
            # Attack phase: gain increases from 0.0 to 1.2
            gain = 1.2 * i / adsr_attack_samples
        elif i < adsr_attack_samples + adsr_decay_samples:
            # Decay phase: gain decreases from 1.2 to 1.0
            # Correct the formula to accurately reflect the decrease
            gain = 1.2 - (0.2 * (i - adsr_attack_samples) / adsr_decay_samples)
        elif i < total_length - adsr_release_samples:
            # Sustain phase: gain remains at 1.0
            gain = 1.0
        else:
            # Release phase: gain decreases from 1.0 to 0.0
            # Ensure the release phase gain calculation correctly scales down to 0
            gain = (total_length - i) / adsr_release_samples
        audio_data[i] *= gain


def audio_stereo_mix_in(stereo_data: Array, channel_data: Array, which_channel: int) -> None:
    """! This function mixes in an audio channel to the stereo audio data.
    
    This function first checks if the number of stereo audio samples (**stereo_data**) is twice the number of input channel data (**channel_data**). If not, it raises an exception. Otherwise, for each sample in **channel_data** (denote it as the **i**-th sample), using the input **which_channel**, this function mixes **channel_data[i]** into **stereo_data** at the position **i** * 2 + **which_channel**, where **which_channel** equal to 0 is the left channel, and 1 is the right channel. When mixing it in, it adds a new value to the existing value.
    
    @param stereo_data The stereo audio data.
    @param channel_data The mono channel audio data to mix in.
    @param which_channel The channel to mix in.
    """
    # Check the length requirement
    if len(stereo_data) != len(channel_data) * 2:
        raise ValueError("Stereo track length must be twice the length of mono track.")
    
    # Mix in the channel data to the specified channel
    for i in range(len(channel_data)):
        stereo_data[i * 2 + which_channel] += channel_data[i]
