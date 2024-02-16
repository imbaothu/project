"""! @brief The Song package.
"""

##
# @file Song.py
#
# @brief This package defines the song class.
#
# @section description_song Description
# This package defines the Song.Song class, which reads the formatted music score and produces a song. The music score is space-separated and formatted as below:
# ```text
# num_of_samples
# num_of_instruments
# wave_type_1 envelope_type_1 instrument_amplitude_1 pan_angle_1
# wave_type_2 envelope_type_2 instrument_amplitude_2 pan_angle_2
# ...
# wave_type_n envelope_type_n instrument_amplitude_n pan_angle_n
# note_1_instrument_index note_1_amplitude note_1_start_sample_index note_1_end_sample_index
# note_2_instrument_index note_2_amplitude note_2_start_sample_index note_2_end_sample_index
# ...
# note_m_instrument_index note_m_amplitude note_m_start_sample_index note_m_end_sample_index
# ```
# The music score specifies how many samples the song has (**num_of_samples**) and how many instruments are used (**num_of_instruments**). For each instrument, it specifies which wave type (**wave_type_x**) should be used to generate the wave sound, which envelope should be applied (**envelope_type_x**), the instrument amplitude (**instrument_amplitude_x**), and the pan angle (**pan_angle_x**). Then, it describes all the notes of a song. Each note has an instrument index (**note_x_instrument_index**), its own amplitude (**note_x_amplitude**), and from which sample (**note_x_start_sample_index**) to which sample (**note_x_end_sample_index**) that the note sounds in the song. For example, below is a simple do-re-mi-fa-so melody described using the above music score format:
# ```text
# 441001
# 1
# 1 2 0.8 0.02
# 0 45 0.63 0 22004
# 0 47 0.63 22050 44054
# 0 48 0.63 44100 66104
# 0 50 0.63 66150 88154
# 0 52 0.63 88200 110204
# 0 53 0.63 110250 132254
# 0 55 0.63 132300 154304
# 0 57 0.63 154350 176354
# 0 59 0.63 176400 198404
# 0 60 0.63 198450 220454
# 0 62 0.63 220500 242504
# 0 64 0.63 242550 264554
# 0 65 0.63 264600 286604
# 0 67 0.63 286650 308654
# 0 69 0.63 308700 330704
# 0 71 0.63 330750 352754
# 0 72 0.63 352800 374804
# 0 74 0.63 374850 396854
# 0 76 0.63 396900 418904
# 0 77 0.63 418950 440954
# ```
# This song has 441001 samples and has only one instrument, which uses Wave.SineWave and ADSR envelope. The instrument amplitude is 0.8, and its pan angle is 0.02. It has 20 notes from notes 45 to 77 and is evenly distributed among the song samples.
#
# To generate a song from this music score, we need to create audio samples for each instrument. Then, for each note, we generate the corresponding sound wave, apply the envelope if needed, and accumulate the sound wave into the audio samples. After processing all the notes for each instrument and at each time position, we compute the averaged value. For example, if there are five notes accumulated to the i-th sample, then the i-th sample should be divided by five. At least, for each instrument, we mix its audio data into stereo song data by using its own amplitude and pan angle.
#
# @section libraries_song Libraries/Modules
# - typing (from the standard library)
#   - access to TextIO, List, and Dict
# - Wave
#   - access to Wave.BaseWave, Wave.SineWave, Wave.SquareWave, Wave.SawtoothWave, Wave.ComplexWave, and Wave.StringWave
# - AudioProcessor
#   - access to audio processing functions
# - DataStructure
#   - access to DataStructure.Array
#
# @section notes_song Notes
# - Comments should be Doxygen compatible.
#
# @section todo_song TODO
# Your task is to implement the Song.Song class that inherits from Wave.BaseWave. The initializer of this class should take one parameter -- the simple formatted music sheet, and use it to render a song accordingly. To break down the song rendering logic, we recommend the below helper methods:
# - Song.Song._read_int(): read a line from the input stream and parse it as an integer.
# - Song.Song._read_instrument_info(): read the instrument information from the input stream.
# - Song.Song._generate_instrument_note_wave(): generate the sound wave for an instrument note.
# - Song.Song._read_instrument_audio_data(): read the instrument audio sample data from the input stream and generate the audio samples.
# - Song.Song._average_audio_data_samples(): average the audio samples (dividing the sampled value by the total number of samples.)
# - Song.Song._mix_instrument_audio_in_song(): mix the multiple instrument audio data into song stereo audio data.
#
# Then the Song's initializer should look like the one below:
# ```python
# with open(song_file, 'r') as in_file:
#     # read the number of samples
#     num_samples = self._read_int(in_file)
#     # read the number of channels
#     num_instruments = self._read_int(in_file)
#     # initialize instrument info
#     instrument_info = [{'wavetype': 1, 'envelope': 0, 'amplitude': 1, 'pan': 0} for _ in range(num_instruments)]
#     # read the instrument info
#     self._read_instrument_info(in_file, instrument_info)
#     # initialize instrument audio data to store the sum of all samples and the number of samples
#     audio_data = [Array(num_samples, 0) for _ in range(num_instruments)]
#     audio_num_samples = [Array(num_samples, 0) for _ in range(num_instruments)]
#     # read the instrument audio data
#     self._read_instrument_audio_data(in_file, instrument_info, audio_data, audio_num_samples)
#     # compute the average of the samples
#     self._average_audio_data_samples(audio_data, audio_num_samples)            
#     # initialize the song audio data, which has two channels for stereo sound
#     super().__init__(num_samples, 2)
#     # mix in instrument audio data into song stereo data
#     self._mix_instrument_audio_in_song(instrument_info, audio_data)
# ```
# However, you are free to implement the Song.Song class in whatever way you want. If you don't like our recommendation, feel free to remove all the methods and implement your own Song.Song class as you desire. As long as it produces the same song, you will obtain the full score.
#
# @section author_song Author(s)
# - Created by SingChun Lee on 12/24/2023
# - Modified by SingChun Lee on 12/30/2023
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

from typing import TextIO, List, Dict
from Wave import *
from AudioProcessor import *
from DataStructure import Array

class Song(BaseWave):
    """! The Song.Song class.
    
    It extends the Wave.BaseWave class and initializes the wave samples by reading a simple formatted music score text file. It reads the music score line by line, generates wave samples notes by notes, and mixes them in stereo audio data.
    """
    
    def __init__(self, song_file: str) -> None:
        """! The Song.Song class initializer.
        
        It opens the input **song_file** as an input stream and parses the music score text file accordingly. It first reads the total number of samples and the number of instruments. Then, it reads the instrument information, including the wave type (1: sine, 2: square, 3: sawtooth, 4: complex, 5: string), which envelope to apply (0: no envelope, 1: rise/fall envelope, 2: ADSR envelope), the wave amplitude, and the pan angle. It is recommended to store in a list of dict. This method then initializes the instrument audio data using Arrays. Since it has multiple instruments, it is suggested to use a list of Arrays. This will store the accumulated sound value of each instrument at each time position. 
        
        Furthermore, in order to compute the average value, it may be a good idea to initialize another list of Arrays to store the total number of samples generated for each instrument at each time position. These two variables are filled by reading notes specified in the music score. For each note read, it generates the corresponding sound wave and accumulates the sound sample in the list of Arrays variables. After reading all notes, it computes the average note value for each instrument at each time position. In the end, it mixes the instrument audio sample data into stereo song data.
        
        @param song_file The input musicscore text file
        """
        
        with open(song_file, 'r') as in_file:
            # read the number of samples
            num_samples = self._read_int(in_file)
            # read the number of instruments
            num_instruments = self._read_int(in_file)
            # initialize instrument info
            instrument_info = [{'wavetype': 1, 'envelope': 0, 'amplitude': 1, 'pan': 0} for _ in range(num_instruments)]
            # read the instrument info
            self._read_instrument_info(in_file, instrument_info)
            # initialize instrument audio data to store the sum of all samples and the number of samples
            audio_data = [Array(num_samples, 0) for _ in range(num_instruments)]
            audio_num_samples = [Array(num_samples, 0) for _ in range(num_instruments)]
            # read the instrument audio data
            self._read_instrument_audio_data(in_file, instrument_info, audio_data, audio_num_samples)
            # compute the average of the samples
            self._average_audio_data_samples(audio_data, audio_num_samples)            
            # initialize the song audio data, which has two channels for stereo sound
            super().__init__(num_samples, 2)
            # mix in instrument audio data into song stereo data
            self._mix_instrument_audio_in_song(instrument_info, audio_data)
                
    def _read_int(self, in_file: TextIO) -> None:
        """! A helper method to read a line from in_file and return it as an integer.
        
        This method reads a line from **in_file**, recasts it as an integer, and returns the recast result.
        
        @param in_file The input file stream.
        """
        
        pass
                
    def _read_instrument_info(self, in_file: TextIO, instrument_info: List[Dict]) -> None:
        """! A helper method to read the instrument information form in_file and store it to instrument_info.
        
        The input **instrument_info** is expected to be a list of dict that represents a list of instrument information. The length of **instrument_info** is the total number of instruments. For each instrument, this method reads a line from **in_file** and splits the read line into values. It assigns and recasts the corresponding values into the dict.
        
        @param in_file The input file stream.
        
        @param instrument_info The output instrument information, which is a list of dict.
        """
        
        pass
                
    def _generate_instrument_note_wave(self, wave_type: int, num_samples: int, freq: float, amp: float) -> BaseWave:
        """! A helper method to generate an instrument note sound wave based on the input wave_type, num_samples, freq, and amp.
        
        This method uses Wave.SineWave, Wave.SquareWave, Wave.SawtoothWave, Wave.ComplexWave, or Wave.StringWave creates a sound wave and returns it. The input **wave_type** determines which class to use to generate the sound wave. All other input parameters are relayed to the Wave class for wave generation. 
        
        @param wave_type The wave type. 1: sine, 2: square, 3: sawtooth, 4: complex, 5: string
        
        @param num_samples The number of samples.
        
        @param freq The wave frequency.
        
        @param amp The wave amplitude.
        
        @return A sound wave.
        """
        
        pass
        
    def _read_instrument_audio_data(self, in_file: TextIO, instrument_info: List[Dict], audio_data: List[Array], audio_num_samples: List[Array]):
        """! A helper method to read the instrument audio data from in_file and store it to audio_data.
        
        This method reads **in_file** line by line until the end. Each line represents a note of an instrument. After splitting the line into values, this method should obtain the instrument index (telling us which instrument the note belongs to), the note number (which can be converted to frequency using audio_note_number_to_freq()), the note amplitude, the starting and ending sample indices. Using this information, this method calls _generate_instrument_note_wave() to create the note sound wave, then applies the envelope, and at last accumulates the samples in **audio_data** (using the instrument index, the starting and ending sample indices). This method also increases the number of sample counters **audio_num_samples** whenever it accumulates a sound sample to **audio_data**.
        
        @param in_file The input file stream.
        
        @param instrument_info The instrument information.
        
        @param audio_data The instrument audio data.
        
        @param audio_num_samples The number of samples of each instrument audio data.
        """
        
        pass
                
    def _average_audio_data_samples(self, audio_data: List[Array], audio_num_samples: List[Array]):
        """! A helper method to compute the average of the audio data by dividing the input audio data by the total number of samples.
        
        This method computes the average sample values. Note that **audio_data** stores the accumulated sample values while **audio_num_samples** stores the total number of samples. To compute the average values, this method loops each instrument and loops each sample data in **audio_data**, then divides the sample value by the total number of samples. Note that this method only divides the sample value by the total number of samples when the total number of samples is not zero.
        
        @param audio_data The instrument audio data.
        
        @param audio_num_samples The number of samples of each instrument audio data.
        """
        
        pass
        
    def _mix_instrument_audio_in_song(self, instrument_info: List[Dict], audio_data: List[Array]):
        """! A helper method to mix the instrument audio data into a stereo sound.
        
        For each instrument (i.e., looping **audio_data**), it uses the pan angle (stored in **instrument_info**) and audio_stereo_gains() to compute the left and right channel gains. Then, it multiples the gains by the instrument amplitude (also stored in **instrument_info**), calls audio_multiply_gain() to apply the gain to the instrument's audio data and calls audio_stereo_mix_in() to mix the instrument's audio data into the song's audio data (i.e., **self._data**).
        
        @param instrument_info The instrument information.
        
        @param audio_data The instrument audio data.
        """
        
        pass