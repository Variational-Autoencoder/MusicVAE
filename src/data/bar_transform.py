import numpy as np
import math

class BarTransform():

    def __init__(self, bars=1, note_count=60):
        self.split_size = bars*16
        self.note_count = note_count

    def get_sections(self, sample_length):
        return math.ceil(sample_length/ self.split_size)

    def __call__(self, sample):
        sample_length = len(sample)

        # Pad the sample with 0's if there's not enough to create equal splits into n bars
        leftover = sample_length % self.split_size
        if leftover != 0:
            padding_size = self.split_size - leftover
            padding = np.zeros((padding_size, self.note_count))
            sample = np.append(sample, padding, axis=0)


        sections = self.get_sections(sample_length)
        # Split into X equal sections
        split_list = np.array_split(sample, indices_or_sections=sections)


        return split_list