import numpy as np
import math

def BarTransform(bars=1, note_count=60):
    split_size = bars*16

    def transform(sample):
        sample_length = len(sample)

        # Pad the sample with 0's if there's not enough to create equal splits into n bars
        leftover = sample_length % split_size
        if leftover != 0:
            padding_size = split_size - leftover
            padding = np.zeros((padding_size, note_count))
            sample = np.append(sample, padding, axis=0)


        sections = math.ceil(sample_length / split_size)
        # Split into X equal sections
        split_list = np.array_split(sample, indices_or_sections=sections)


        return split_list

    return transform