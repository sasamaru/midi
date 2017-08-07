#楽器の指定、noteの指定などについての練習
import pretty_midi

midi_data = pretty_midi.PrettyMIDI('making/level_up.mid')


# instrument には,
# program : int ,,,MIDI program number (instrument index), in [0, 127]
# is_drum : bool
# name : str
# の3つがあるみたいだけど、元々のやつにはnameはnullらしい。

for instrument in midi_data.instruments:
    if not instrument.name:
        for note in instrument.notes:
        	#どうやら, pretty_midi.Noteのインスタンスnoteについて
			#note.pitchで音程を変更できるようだ。
            note.pitch += 15

midi_data.write('making/level_up3.mid')