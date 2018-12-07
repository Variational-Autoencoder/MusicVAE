import pandas as pd
import pretty_midi

import matplotlib.pyplot as plt
import librosa.display as display

class MidiBuilder():
    """Build a MIDI from a piano roll sample"""

    def __init__(self, midi_start=48, midi_end=108):
        """
        Args:
            midi_start (int): The first midi note in the dataset
            midi_end (int): The last midi note in the dataset
        """
        self.dtypes = {'piano_roll_name': 'object', 'timestep': 'uint32'}
        self.column_names = [pretty_midi.note_number_to_name(n) for n in range(midi_start, midi_end)]
        for column in self.column_names:
            self.dtypes[column] = 'uint8'


    def midi_from_piano_roll(self, sample, tempo = 120):
        """
            We're taking some assumptions here to reconstruct the midi.
        """
        piano_roll = pd.DataFrame(sample, columns=self.column_names, dtype='uint8')

        program = 0
        velocity = int(100)
        bps = tempo / 60
        sps = bps * 4 # sixteenth notes per second

        # Create a PrettyMIDI object
        piano_midi = pretty_midi.PrettyMIDI()

        piano = pretty_midi.Instrument(program=program)
        # Iterate over note names, which will be converted to note number later
        for idx in piano_roll.index:
            for note_name in piano_roll.columns:
                #print(note_name)

                # Check if the note is activated at this timestep
                if piano_roll.iloc[idx][note_name] == 1.:
                    # Retrieve the MIDI note number for this note name
                    note_number = pretty_midi.note_name_to_number(note_name)

                    note_start = idx/sps # 0 if tempo = 60
                    note_end = (idx+1)/sps # 0.25

                    # Create a Note instance, starting according to the timestep * 16ths, ending one sixteenth later
                    # TODO: Smooth this a bit by using lookahead
                    note = pretty_midi.Note(
                        velocity=velocity, pitch=note_number, start=note_start, end=note_end)
                    # Add it to our instrument
                    piano.notes.append(note)
        # Add the instrument to the PrettyMIDI object
        piano_midi.instruments.append(piano)
        return piano_midi

        # Write out the MIDI data
        #piano_midi.write('name.mid')

    def plot_midi(self, midi_sample):
        display.specshow(midi_sample.get_piano_roll(), y_axis='cqt_note', cmap=plt.cm.hot)

    def play_midi(self, midi_sample):
        fs = 44100
        synth = midi_sample.synthesize(fs=fs)
        return [synth], fs