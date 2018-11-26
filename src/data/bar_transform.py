import numpy as np
import math

def BarTransform(bars=1, note_count=60):
    split_size = bars*16

    def transform(sample):
        sections = math.ceil(len(sample) / split_size)
        # Split into X equal sections
        split_list = np.array_split(sample, indices_or_sections=sections)

        # Pad the last section with zeroes if necessary
        last_elem_size_diff = split_size - len(split_list[-1])

        if last_elem_size_diff > 0:
            for i in range(0, last_elem_size_diff):
                split_list[-1] = np.vstack((split_list[-1], np.zeros(note_count)))

        return split_list

    return transform
