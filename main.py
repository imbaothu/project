##
# @mainpage Audio Processing
#
# @section description_audioprocessing Description
# Check the project instruction on [Gradescope](https://www.gradescope.com/courses/711657/assignments/3972408).
#
# @section acknowledgement_audioprocessing Acknowledgement
# - This project is adapted from [Prof. David H. Hovemeyer](https://www.cs.jhu.edu/~daveho/) Fall 2019 C midterm project at JHU: https://github.com/jhuintprog/fall2019
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

"""! @brief The main program of project 1 - audio processing.
"""

##
# @file main.py
#
# @brief Project 1 main program
#
# @section description_main Description
# This is the main program of Project 1. You should run this program, select the option that corresponding to the function that you have implemented, and use it to verify your program output. For example, after implementing AudioProcessor.audio_generate_sine_wave(), you can run:
#
#     python main.py
#
# and select 1) Create a simple sine wave tone, and input number of samples: 44100, frequency: 261.63, and output filename: my_sine_c.wav. It should produce a sound similar to <A HREF="rss/sine_c.wav">this one</A>.
#
# Futhermore, you can compare the two wave files by running:
#
#     python main.py sine_c.wav my_sine_c.wav
#
# If your implementation is correct, you should see the below output:
#
# ```console
# Comparing .\tests\sine_c.wav and .\tests\my_sine_c.wav
# Files are identical!
# ```   
# 
# Otherwise, you may see something similar to this:
#
# ```console
# Comparing .\tests\sine_c.wav and .\tests\my_sine_c.wav
# Number of samples (> 0.001): 43996
# Number of samples (> 0.01): 43226
# Number of samples (> 0.1): 38370
# Number of samples (> 0.2): 34063
# ```
#
# It tells you how many samples are different more than 0.001, 0.01, 0.1, and 0.2. If your results and ours have minor differences (< 0.01), that is acceptable. However, you should aim on having no differences (i.e. < 0.001). To help with the comparison, here are the options and their corresponding wave files.
# | Main Menu | Parameters  | Result File |
# | ----------| ----------- | ----------- |
# | 1         | samples: 44100, freq: 261.63     | <A HREF="rss/sine_c.wav">sine_c.wav</A> |
# | 2         | samples: 44100, freq: 493.88     | <A HREF="rss/square_b.wav">square_b.wav</A> |
# | 3         | samples: 44100, freq: 392.0      | <A HREF="rss/sawtooth_g.wav">sawtooth_g.wav</A> |
# | 4         | samples: 44100, freq: 493.88     | <A HREF="rss/complex_b.wav">complex_b.wav</A> |
# | 5         | samples: 44100, freq: 329.63     | <A HREF="rss/string_e.wav">string_e.wav</A> |
# | 6         | file: sine_c.wav, angle: 0.18    | <A HREF="rss/sine_c_stereo.wav">sine_c_stereo.wav</A> |
# | 6         | file: square_b.wav, angle: 0.29  | <A HREF="rss/square_b_stereo.wav">square_b_stereo.wav</A> |
# | 6         | file: sawtooth_g.wav, angle: 0.05| <A HREF="rss/sawtooth_g_stereo.wav">sawtooth_g_stereo.wav</A> |
# | 6         | file: complex_b.wav, angle: -0.07| <A HREF="rss/complex_b_stereo.wav">complex_b_stereo.wav</A> |
# | 6         | file: string_e.wav, angle: -0.14 | <A HREF="rss/string_e_stereo.wav">string_e_stereo.wav</A> |
# | 7         | file: sine_c.wav                 | <A HREF="rss/sine_c_rf.wav">sine_c_rf.wav</A> |
# | 7         | file: square_b.wav               | <A HREF="rss/square_b_rf.wav">square_b_rf.wav</A> |
# | 8         | file: sawtooth_g.wav             | <A HREF="rss/sawtooth_g_adsr.wav">sawtooth_g_adsr.wav</A> |
# | 8         | file: complex_b.wav              | <A HREF="rss/complex_b_adsr.wav">complex_b_adsr.wav</A> |
# | 8         | file: string_e.wav               | <A HREF="rss/string_e_adsr.wav">string_e_adsr.wav</A> |
# | 9         | file: simple.txt                 | <A HREF="rss/simple.wav">simple.wav</A> |
# | 9         | file: dear_bucknell.txt          | <A HREF="rss/dear_bucknell.wav">dear_bucknell.wav</A> |
# | 9         | file: zelda_main_theme.txt       | <A HREF="rss/zelda_main_theme.wav">zelda_main_theme.wav</A> |
# | 9         | file: toccata_fugue_d_minor.txt  | <A HREF="rss/toccata_fugue_d_minor.wav">toccata_fugue_d_minor.wav</A> |
#
# Note: it may take minutes to generate the song Toccata Fugue in D Minor.
#
# @section libraries_main Libraries/Modules
# - sys (from the standard library)
#   - access to command line arguments
# - typing (from the standard library)
#   - access to Tuple
# - Wave
#   - access to Wave.BaseWave, Wave.SineWave, Wave.SquareWave, Wave.SawtoothWave, Wave.ComplexWave, and Wave.StringWave
# - AudioProcessor
#   - access to audio processing functions
# - Song
#   - access to Song.Song
#
# @section notes_main Notes
# - Comments should be Doxygen compatible.
#
# @section toto_main TODO
# - None. You should not need to modify this file. If you do, write it down in the README and let us know why you need to make the changes.
#
# @section author_main Author(s)
# - Created by SingChun Lee on 12/24/2023
# - Modified by SingChun Lee on 12/30/2023
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

from sys import argv
from typing import Tuple
from Wave import *
from AudioProcessor import *
from Song import *

def print_main_menu() -> int:
    """! This function prints the main menu and gets user's selection.
    
    This function displays nine options for users to select. It asks for the user input and returns an integer from 1 to 9 to represent the user's selection.
    
    @return An integer that represents the user selection.
    """
    
    print("Select one of the below test options:")
    print("\t1) Create a simple sine wave tone")
    print("\t2) Create a simple square wave tone")
    print("\t3) Create a simple sawtooth wave tone")
    print("\t4) Create a simple complex wave tone")
    print("\t5) Create a simple string wave tone")
    print("\t6) Apply stereo")
    print("\t7) Apply rise/fall envelope")
    print("\t8) Apply ADSR envelope")
    print("\t9) Generate a song")
    print("\n")
    return int(input("Enter [1-9]: "))

def get_wave_parameters() -> Tuple[int, int]:
    """! This function gets the number of samples and wave frequency from the user.
    
    This function asks the user to provide two integer inputs that specify the number of samples and wave frequency of the generating sound. It returns the user's input as a tuple.
    
    @return The number of samples and wave frequency.
    """
    
    num_samples = input("Number of samples: ")
    freq = input("Wave frequency: ")
    return int(num_samples), float(freq)

def get_filename(ask_for_input: bool = False) -> str:
    """! This function gets the input/output filename from the user.
    
    This function takes a boolean parameter, which decides to ask for input or output filename, and asks the user to input a filename. It returns the user's input.
    
    @param ask_for_input A parameter to determine printing "input" or "output"
    
    @return The input/output filename.
    """
    
    return input(("Input" if ask_for_input else "Output") + " file: ")

def create_waveform(wave_type: int) -> None:
    """! This function write a digital waveform to a wave file based on the input wave_type.

    This function takes an input parameter wave_type, which represents sine (1), square (2), sawtooth (3), complex (4), and string (5), and it calls get_wave_parameters() to get the desired number of samples and wave frequency and get_filename() to get the output filename, then creates and write the corresponding wave sound to a wave file.
    
    @param wave_type 1: sine wave, 2: square wave, 3: sawtooth wave, 4: complex wave, 5: string wave.
    """
    
    num_samples, freq = get_wave_parameters()
    filename = get_filename()
    if wave_type == 1: wave = SineWave(num_samples, freq) 
    elif wave_type == 2: wave = SquareWave(num_samples, freq) 
    elif wave_type == 3: wave = SawtoothWave(num_samples, freq)
    elif wave_type == 4: wave = ComplexWave(num_samples, freq)
    else: wave = StringWave(num_samples, freq)
    wave.write_wave_file(filename)

def apply_stereo() -> None:
    """! This function creates a stereo version of an input mono wave sound.
    
    This function calls get_filename() to get an input wave file and an output filename and asks the user to provide a stereo pan angle. Then, it reads the input wave file, computes the pan angle, and mixes the mono wave sound into a stereo wave sound. At last, it writes the stereo sound to the specified output wave file.
    """
    
    in_filename = get_filename(True)
    angle = float(input("Angle: "))
    out_filename = get_filename()
    wave_left = BaseWave(filename = in_filename)
    wave_right = BaseWave(filename = in_filename)
    gain_left, gain_right = audio_stereo_gains(angle)
    audio_multiply_gain(wave_left._data, gain_left)
    audio_multiply_gain(wave_left._data, gain_right)
    wave = BaseWave(len(wave_left._data), 2)
    audio_stereo_mix_in(wave._data, wave_left._data, 0)
    audio_stereo_mix_in(wave._data, wave_right._data, 1)
    wave.write_wave_file(out_filename)

def apply_rise_fall_envelope() -> None:
    """! This function applies the rise-fall envelope to an input wave sound.
    
    This function calls get_filename() to get an input wave file and an output filename, then it calls audio_rise_fall_envelope() to apply the rise-fall envelope to the input wave sound. At last, it writes the resulting sound to the specified output file.
    """
    
    in_filename = get_filename(True)
    out_filename = get_filename(False)
    wave = BaseWave(filename = in_filename)
    audio_rise_fall_envelope(wave._data)
    wave.write_wave_file(out_filename)

def apply_adsr_envelope() -> None:
    """! This function applies the ADSR envelope to an input wave sound.
    
    This function calls get_filename() to get an input wave file and an output filename, then it calls audio_adsr_envelope() to apply the ADSR envelope to the input wave sound. Finally, it writes the resulting sound to the specified output file.
    """
    
    in_filename = get_filename(True)
    out_filename = get_filename(False)
    wave = BaseWave(filename = in_filename)
    audio_adsr_envelope(wave._data)
    wave.write_wave_file(out_filename)
    
def generate_song() -> None:
    """! This function generates a song from a simple formatted music sheet.
    
    This function calls get_filename() to get an input simple formatted music sheet and an output filename, then uses the Song.Song class to generate a song and write the song to the specified output file.
    """
    
    in_filename = get_filename(True)
    out_filename = get_filename(False)
    wave = Song(in_filename)
    wave.write_wave_file(out_filename)

def compare_two_wave_files(file1: str, file2: str) -> None:
    """! This function compares two wave files and reports the differences.
    
    This function reads the two input wave files and first compares if they have the same number of samples. Then, it compares how many samples differ by more than 0.001, 0.01, 0.1, and 0.2. It reports all the differences. If there is no difference, it reports that the two files are identical.
    
    @param file1 The first wave file.
    
    @param file2 The second wave file.
    """
    
    print("Comparing " + file1 + " and " + file2)
    wave1 = BaseWave(filename = file1)
    wave2 = BaseWave(filename = file2)
    if len(wave1._data) != len(wave2._data):
        print("The number of samples does not match: " + str(len(wave1._data)) + " vs " + str(len(wave2._data)))
    min_num = min(len(wave1._data), len(wave2._data))
    diffs = { 0.001: 0, 0.01: 0, 0.1: 0, 0.2: 0 }
    for i in range(min_num):
        diff = abs(wave1._data[i] - wave2._data[i])
        for key in diffs.keys():
            if diff > key: diffs[key] += 1
    has_diff = False
    for key, val in diffs.items():
        if val > 0:
            print("Number of samples (> " + str(key) + "): " + str(val))
            has_diff = True
    if not has_diff: print("Files are identical!")

def main() -> None:
    """! Project 1 Main Program
    
    This is the main program of Project 1. It has the following two usages:
    
        python main.py    and    python main.py wave_file_1 wave_file 2
        
    When it takes no command line arguments, it runs print_main_menu() and creates wave files according to the user's choices. On the other hand, when it takes two command line arguments, it assumes the two inputs are two wave filenames, and the program will compare the two files by calling compare_two_wave_files(). Otherwise, this function will print the program usage.
    """
    
    args = argv[1:]
    if len(args) == 0:
        main_option = 0
        while main_option < 1 or main_option > 9:
            try:
                main_option = print_main_menu()
            except Exception:
                print("Invalid input! Please try again.")
        if main_option == 1: create_waveform(1)
        elif main_option == 2: create_waveform(2)
        elif main_option == 3: create_waveform(3)
        elif main_option == 4: create_waveform(4)
        elif main_option == 5: create_waveform(5)
        elif main_option == 6: apply_stereo()
        elif main_option == 7: apply_rise_fall_envelope()
        elif main_option == 8: apply_adsr_envelope()
        elif main_option == 9: generate_song()
        
    elif len(args) == 2:
        file1 = args[0]
        file2 = args[1]
        if ".wav" in file1 and ".wav" in file2:
            compare_two_wave_files(file1, file2)
    else:
        print("\nTo compare two wave files: python main.py wave_file_1 wave_file_2")
        print("\n\tOR\n")
        print("To test audio processing: python main.py\n")

if __name__ == "__main__":
    main()
