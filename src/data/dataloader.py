import pandas as pd
from torch.utils.data import Dataset, DataLoader
import pretty_midi

class MidiDataset(Dataset):
    """Pre-processed MIDI dataset."""

    def __init__(self, csv_file, transform=None, midi_start=48, midi_end=108):
        """
        Args:
            csv_file (string): Path to the csv file with piano rolls per song.
            transform (callable, optional): Optional transform to be applied
                on a sample.
            midi_start (int): The first midi note in the dataset
            midi_end (int): The last midi note in the dataset
        """
        dtypes = {'piano_roll_name': 'object', 'timestep': 'uint32'}
        column_names = [pretty_midi.note_number_to_name(n) for n in range(midi_start, midi_end)]
        for column in column_names:
            dtypes[column] = 'uint8'

        self.piano_rolls = pd.read_csv(csv_file, sep=';', index_col=['piano_roll_name', 'timestep'], dtype=dtypes)
        self.transform = transform

    def __len__(self):
        return len(self.piano_rolls.index.levels[0])

    def get_mem_usage(self):
        """
            Returns the memory usage in MB
        """
        return self.piano_rolls.memory_usage(deep=True).sum() / 1024**2

    def get_indexer(self):
        """
            Get an indexer that treats each first level index as a sample.
        """
        return self.piano_rolls.index.get_level_values(0).unique()

    def __getitem__(self, idx):
        """
            Our frame is multi-index, so we're thinking each song is a single sample,
            and getting the individual bars is a transform of that sample?
        """
        indexer = self.get_indexer()

        piano_rolls = self.piano_rolls.loc[indexer[idx]].values
        piano_rolls = piano_rolls.astype('float')

        sample = {'piano_rolls': piano_rolls}

        if self.transform is not None:
            sample['piano_rolls'] = self.transform(piano_rolls)

        return sample
