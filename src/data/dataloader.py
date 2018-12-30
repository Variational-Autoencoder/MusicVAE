import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import pretty_midi

class MidiDataset(Dataset):
    """Pre-processed MIDI dataset."""

    def __init__(self, csv_file, transform, midi_start=48, midi_end=108):
        """
        Args:
            csv_file (string): Path to the csv file with piano rolls per song.
            transform (callable): Transform to be applied on a sample, is expected to implement "get_sections".
            midi_start (int): The first midi note in the dataset
            midi_end (int): The last midi note in the dataset
        """

        dtypes = {'piano_roll_name': 'object', 'timestep': 'uint32'}
        column_names = [pretty_midi.note_number_to_name(n) for n in range(midi_start, midi_end)]
        for column in column_names:
            dtypes[column] = 'uint8'

        self.piano_rolls = pd.read_csv(csv_file, sep=';', index_col=['piano_roll_name', 'timestep'], dtype=dtypes)
        self.transform = transform

        self.init_dataset()

    def init_dataset(self):
        """
            Sets up an array containing a pd index (the song name) and the song section,
            ie. [("Song Name:1", 0), ("Song Name:1", 1), ("Song Name:1", 2)]
            for use in indexing a specific section
        """
        indexer = self._get_indexer()

        self.index_mapper = []
        for i in indexer:
            split_count = self.transform.get_sections(len(self.piano_rolls.loc[i].values))
            for j in range(0, split_count):
                self.index_mapper.append((i, j))


    def __len__(self):
        return len(self.index_mapper)

    def get_mem_usage(self):
        """
            Returns the memory usage in MB
        """
        return self.piano_rolls.memory_usage(deep=True).sum() / 1024**2

    def _get_indexer(self):
        """
            Get an indexer that treats each first level index as a sample.
        """
        return self.piano_rolls.index.get_level_values(0).unique()

    def __getitem__(self, idx):
        """
            Our frame is multi-index, so we're thinking each song is a single sample,
            and getting the individual bars is a transform of that sample?
        """
        song_name, section = self.index_mapper[idx]

        # Add a column for silences
        piano_rolls = self.piano_rolls.loc[song_name].values
        silence_col = np.zeros((piano_rolls.shape[0], 1))
        piano_rolls_with_silences = np.append(piano_rolls, silence_col, axis=1)

        # Transform the sample (including padding)
        sample = piano_rolls_with_silences.astype('float')
        sample = self.transform(sample)[section]

        # Fill in 1's for the silent rows
        empty_rows = ~sample.any(axis=1)
        if len(sample[empty_rows]) > 0:
            sample[empty_rows, -1] = 1.

        sample = {'piano_rolls': sample}

        return sample
