import pretty_midi
# Create a PrettyMIDI object
# MIDIを作る
# 引数が、
# PrettyMIDI(midi_file=None, resolution=220, initial_tempo=120.0)
# である。
# cello_c_chord = pretty_midi.PrettyMIDI(initial_tempo=200.0)
# のように設定。 
cello_c_chord = pretty_midi.PrettyMIDI()

# Create an Instrument instance for a cello instrument
# チェロのインスタンスを作る
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)
cello2 = pretty_midi.Instrument(program=cello_program)
cello3 = pretty_midi.Instrument(program=cello_program)
cello4 = pretty_midi.Instrument(program=cello_program)
cello5 = pretty_midi.Instrument(program=cello_program)

# Iterate over note names, which will be converted to note number later
# 繰り返す使うので、['C5', 'E5', 'G5']に名前をつける。
# 音符に名前をつけている。for in は配列のfor文
for note_name in ['C5', 'E5', 'G5']:
# words = ['Japanese', 'English', 'French']
# for w in words:
#     print (w)
# で、Japanese English French が出力。

    # Retrieve the MIDI note number for this note name
    # C5などから、midiで用いる形に変換している。
    note_number = pretty_midi.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    # ここで、音符の設定。 start~endまでを、pitchの音程で再生する。
    # pitchはint,floatで、周波数的な何か？ これを使わず、note_name_to_numberを使うのが良さそう。
    # verocityは謎。
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.5)
    note2 = pretty_midi.Note(velocity=100, pitch=note_number, start=.6, end=.8)
    note3 = pretty_midi.Note(velocity=100, pitch=50, start=.0, end=.5)
    note4 = pretty_midi.Note(velocity=120, pitch=50, start=.6, end=.9)
    note5 = pretty_midi.Note(velocity=120, pitch=50, start=0, end=.5)
    note6 = pretty_midi.Note(velocity=50, pitch=50, start=0, end=.5)

    # Add it to our cello instrument
    # 音符を各楽器に割り当てる。
    cello.notes.append(note)
    cello2.notes.append(note2)
    cello3.notes.append(note3)
    cello3.notes.append(note4)
    cello4.notes.append(note5)
    cello5.notes.append(note6)

# Add the cello instrument to the PrettyMIDI object
#これで、楽器を追加する。上の作業ではまだ楽器がmidiの演奏内に追加されていない。
cello_c_chord.instruments.append(cello)
cello_c_chord.instruments.append(cello2)
cello_c_chord.instruments.append(cello3)
cello_c_chord.instruments.append(cello4)
cello_c_chord.instruments.append(cello5)

# Write out the MIDI data
cello_c_chord.write('making/cello-C-chord.mid')