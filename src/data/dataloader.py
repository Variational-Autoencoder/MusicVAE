import pandas as pd
from torch.utils.data import Dataset, DataLoader

class MidiDataset(Dataset):
    """Pre-processed MIDI dataset."""

    def __init__(self, csv_file, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with piano rolls per song.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.piano_rolls = pd.read_csv(csv_file, sep=';', index_col=['piano_roll_name', 'timestep'])
        self.transform = transform

    def __len__(self):
        return len(self.piano_rolls.index.levels[0])

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
