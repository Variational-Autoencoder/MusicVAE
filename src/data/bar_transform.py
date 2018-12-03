import numpy as np
import math

class BarTransform():

    def __init__(self, bars=1, note_count=60):
        self.split_size = bars*16
        self.note_count = note_count

    def __call__(self, sample):
        sample_length = len(sample)

        # Pad the sample with 0's if there's not enough to create equal splits into n bars
        leftover = sample_length % self.split_size
        if leftover != 0:
            padding_size = self.split_size - leftover
            padding = np.zeros((padding_size, self.note_count))
            sample = np.append(sample, padding, axis=0)


        sections = math.ceil(sample_length / self.split_size)
        # Split into X equal sections
        split_list = np.array_split(sample, indices_or_sections=sections)


        return split_list