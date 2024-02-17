"""! @brief The Wave package.
"""

##
# @file Wave.py
#
# @brief This package defines the wave classes.
#
# @section description_wave Description
# This package provides classes to represent wave sounds. It contains a base wave class and five different basic wave sounds: sine, square, sawtooth, complex, and string waves. The base wave class (BaseWave) provides the wave file read/write functionalities, while the derived wave classes (SineWave, SquareWave, SawtoothWave, ComplexWave, StringWave) use the audio processing functions that you should have implemented in AudioProcessor to generate the corresponding sound waves. You should not need to modify this file. However, you should study this file and learn the OOP modeling and the doxygen-style docstring.
#
# @section libraries_wave Libraries/Modules
# - DataStructure
#   - access to DataStructure.Array
# - AudioProcessor
#   - access to audio processing functions
#
# @section notes_wave Notes
# - Comments should be Doxygen compatible.
#
# @section todo_wave TODO
# - None. You should not need to modify this file. If you do, write it down in the README and let us know why you need to make the changes.
#
# @section author_wave Author(s)
# - Created by SingChun Lee on 12/24/2023
# - Modified by SingChun Lee on 12/30/2023
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

from DataStructure import Array
from AudioProcessor import *

class BaseWave:
    """! The Wave.BaseWave class.
    
    This class defines the base class for sound waves using the wave format defined in http://soundfile.sapp.org/doc/WaveFormat/. It provides the wave file read/write functionalities compatible with the wave file format.
    """
    
    ## The number of samples per second
    samples_per_second = 44100
    
    def __init__(self, num_samples: int = 0, num_channels: int = 1, filename: str = None) -> None:
        """! The BaseWave class initializer.
        
        It initializes the attributes required for the read/write wave file (**_num_channels**, **_byte_rate**, **_block_align**, **_sub_chucksize1**, **_sub_chucksize2**, **_chucksize**, and **_data**). Notice that **_data** is an Array that stores the wave samples. This is the attribute that you will modify when creating sounds. This initializer will also read and initialize the data from a wave file, should **filename** not None.
        
        @param num_samples The number of wave samples. Default is 0.
        
        @param num_channels The number of wave channels. Default is 2.
        
        @param filename The input filename. Default is None.
        """
        
        ## The number of wave channels
        self._num_channels = num_channels
        ## The byte rate
        self._byte_rate = BaseWave.samples_per_second * self._num_channels * 2
        ## The block alignment offset
        self._block_align = self._num_channels * 2
        ## The wave sub-chunksize 1. Ref: http://soundfile.sapp.org/doc/WaveFormat/
        self._sub_chucksize1 = 16
        ## The wave sub-chucksize 2. Ref: http://soundfile.sapp.org/doc/WaveFormat/
        self._sub_chucksize2 = num_samples * self._num_channels * 2
        ## The total wave chuck size.
        self._chucksize = 4 + (8 + self._sub_chucksize1) + (8 + self._sub_chucksize2)
        ## The wave data
        self._data = Array(num_samples * self._num_channels, 0)
        if filename: # if there is an input filename, read from the file
            self.read_wave_file(filename)
    
    def __str__(self) -> str:
        """! A string representation of the base wave class.
        
        It provides a string representation of the wave class. It prints the values of all the attributes except **_data**. For **_data**, it prints the size of the Array instead.
        
        @return A string that represents the base wave class.
        """
        
        # print the wave class attributes
        s = 'Num channels: ' + str(self._num_channels) + '\n'
        s += 'Byte rate: ' + str(self._byte_rate) + '\n'
        s += 'Block align: ' + str(self._block_align) + '\n'
        s += 'Sub-chuck size 1: ' + str(self._sub_chucksize1) + '\n'
        s += 'Sub-chuck size 2: ' + str(self._sub_chucksize2) + '\n'
        s += 'Chuck size: ' + str(self._chucksize) + '\n'
        s += 'Num data: ' + str(len(self._data)) + '\n'
        return s
    
    def write_wave_file(self, filename: str) -> None:
        """! Write to a wave file.
        
        According to the wave file format defined in http://soundfile.sapp.org/doc/WaveFormat/, this method writes the sound wave to a binary wave file that can be played in the ordinary music player.
        
        @param filename The output filename
        """
        with open(filename, "wb") as out_file:
            # write Wave file header - RIFF
            out_file.write(b'RIFF')
            # write Wave file header - the chuck size
            out_file.write(self._chucksize.to_bytes(4, byteorder='little', signed=False))
            # write Wave file header - WAVE
            out_file.write(b'WAVE')
            # write Wave file header - fmt 
            out_file.write(b'fmt ') # sub-chuck1 ID
            # write the sub-chucksize 1
            out_file.write(self._sub_chucksize1.to_bytes(4, byteorder='little', signed=False))
            # write the PCM format
            out_file.write((1).to_bytes(2, byteorder='little', signed=False))
            # write the number of channels
            out_file.write(self._num_channels.to_bytes(2, byteorder='little', signed=False))
            # write the samples rate
            out_file.write(BaseWave.samples_per_second.to_bytes(4, byteorder='little', signed=False))
            # write the byte rate
            out_file.write(self._byte_rate.to_bytes(4, byteorder='little', signed=False))
            # write the block alignment
            out_file.write(self._block_align.to_bytes(2, byteorder='little', signed=False))
            # write the rate of bits per sample
            out_file.write((16).to_bytes(2, byteorder='little', signed=False))
            # write Wave file header - data
            out_file.write(b'data') # sub-chuck2 ID
            # write the sub-chucksize 2
            out_file.write(self._sub_chucksize2.to_bytes(4, byteorder='little', signed=False))
            # write the wave data
            for data in self._data:
                # clipped the value to  [-1, 1]
                clipped_data = min(1, max(-1, data))
                # convert to [-32768, 32767] -- i.e. 16 bits int
                clipped_data = int(clipped_data * (32768 if clipped_data < 0 else 32767))
                # write to the binary file using 2 bytes (16 bits)
                out_file.write(clipped_data.to_bytes(2, byteorder='little', signed=True))
        
    def read_wave_file(self, filename: str) -> None:
        """! Read from a wave file.
        
        According to the wave file format defined in http://soundfile.sapp.org/doc/WaveFormat/, this method reads the sound wave data from a binary wave file and uses it to initialize the corresponding attributes.
        
        @param filename The input filename
        """
        
        with open(filename, "rb") as in_file:
            # read first 4 bytes - RIFF
            string = str(in_file.read(4), encoding='utf-8')
            if string != "RIFF":
                raise Exception("Bad WAV header - RIFF!")
            # read the chuck size
            self._chucksize = int.from_bytes(in_file.read(4), byteorder='little', signed=False)
            # read another 4 bytes - WAVE
            string = str(in_file.read(4), encoding='utf-8')
            if string != "WAVE":
                raise Exception("Bad WAV header - WAVE!")
            # read another 4 bytes - fmt 
            string = str(in_file.read(4), encoding='utf-8')
            if string != "fmt ":
                raise Exception("Bad WAV header - fmt !")
            # read sub-chucksize 1
            self._sub_chucksize1 = int.from_bytes(in_file.read(4), byteorder='little', signed=False)
            # read the PCM format
            audio_format = int.from_bytes(in_file.read(2), byteorder='little', signed=False)
            if audio_format != 1:
                raise Exception("Bad WAV header - PCM Format!")
            # read the number of channels
            self._num_channels = int.from_bytes(in_file.read(2), byteorder='little', signed=False)
            # read the samples rate
            _ = int.from_bytes(in_file.read(4), byteorder='little', signed=False)
            # read the byte rate
            self._byte_rate = int.from_bytes(in_file.read(4), byteorder='little', signed=False)
            # read the block alignment
            self._block_align = int.from_bytes(in_file.read(2), byteorder='little', signed=False)
            # read the rate of bits per sample
            _ = int.from_bytes(in_file.read(2), byteorder='little', signed=False)
            # read another 4 bytes - data
            string = str(in_file.read(4), encoding='utf-8')
            if string != "data":
                raise Exception("Bad WAV header - data!")
            # read sub-chucksize 2
            self._sub_chucksize2 = int.from_bytes(in_file.read(4), byteorder='little', signed=False)
            # read the wave data
            num_data = self._sub_chucksize2 // 2
            self._data = Array(num_data, 0)
            for i in range(num_data):
                int_val = int.from_bytes(in_file.read(2), byteorder='little', signed=True)
                self._data[i] = int_val / (32768 if int_val < 0 else 32767)
                
class SineWave(BaseWave):
    """! The Wave.SineWave class.
    
    It extends the Wave.BaseWave class by initializing a sine wave sound.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The SineWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a sine wave by calling audio_generate_sine_wave().
        
        @param num_samples The number of sine wave samples.
        
        @param wave_freq The sine wave frequency.
        
        @param amplitude The sine wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_sine_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)     
        
class SquareWave(BaseWave):
    """! The Wave.SquareWave class.
    
    It extends the Wave.BaseWave class by initializing a square wave sound.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The SquareWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a square wave by calling audio_generate_square_wave().
        
        @param num_samples The number of square wave samples.
        
        @param wave_freq The square wave frequency.
        
        @param amplitude The square wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_square_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)

''' 
class TriangleWave(BaseWave):
    """! The Wave.TriangleWave class.
    
    It extends the Wave.BaseWave class by initializing a triangle wave sound.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The TriangleWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a triangle wave by calling audio_generate_triangle_wave().
        
        @param num_samples The number of triangle wave samples.
        
        @param wave_freq The triangle wave frequency.
        
        @param amplitude The triangle wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_triangle_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)
 '''
 
class SawtoothWave(BaseWave):
    """! The Wave.SawtoothWave class.
    
    It extends the Wave.BaseWave class by initializing a sawtooth wave sound.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The SawtoothWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a sawtooth wave by calling audio_generate_sawtooth_wave().
        
        @param num_samples The number of sawtooth wave samples.
        
        @param wave_freq The sawtooth wave frequency.
        
        @param amplitude The sawtooth wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_sawtooth_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)
            
class ComplexWave(BaseWave):
    """! The Wave.ComplexWave class.
    
    It extends the Wave.BaseWave class by initializing a complex wave sound.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The ComplexWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a complex wave by calling audio_generate_complex_wave().
        
        @param num_samples The number of complex wave samples.
        
        @param wave_freq The complex wave frequency.
        
        @param amplitude The complex wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_complex_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)
            
class StringWave(BaseWave):
    """! The Wave.StringWave class.
    
    It extends the Wave.BaseWave class by initializing a string wave sound using the Karplus-Strong algorithm.
    """
    
    def __init__(self, num_samples: int, wave_freq: float, amplitude: float = 0.8) -> None:
        """! The StringWave class initializer.
        
        The initializer reuses the base class initializer, takes the number of samples, wave frequency, and wave amplitude as the input parameters, and uses them to initialize a string wave by calling audio_generate_string_wave().
        
        @param num_samples The number of string wave samples.
        
        @param wave_freq The string wave frequency.
        
        @param amplitude The string wave amplitude. Default is 0.8.
        """
        
        super().__init__(num_samples)
        audio_generate_string_wave(self._data, wave_freq, amplitude, BaseWave.samples_per_second)
            
