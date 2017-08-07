# wiki
# http://craffel.github.io/pretty-midi/#pretty-midi-prettymidi

import pretty_midi

pm = pretty_midi.PrettyMIDI(resolution=960, initial_tempo=120) #pretty_midiオブジェクトを作ります
instrument = pretty_midi.Instrument(0) #instrumentはトラックみたいなものです。
instrument2 = pretty_midi.Instrument(1) #instrumentはトラックみたいなものです。

note_number = pretty_midi.note_name_to_number('G4')
note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=1) #noteはNoteOnEventとNoteOffEventに相当します。

instrument.notes.append(note)
pm.instruments.append(instrument)
pm.write('making/test.mid')


################################################################
#
# MIDIファイルの解析、操作、および合成の使用例：
#
################################################################

#midiをロード
midi_data = pretty_midi.PrettyMIDI('making/test.mid')
# Print an empirical estimate of its global tempo
#速さを出力する
print midi_data.estimate_tempo()

# Compute the relative amount of each semitone across the entire song,
# a proxy for key
#全体の各半音の相対的な量を計算します。
#鍵のプロキシ
total_velocity = sum(sum(midi_data.get_chroma()))
print [sum(semitone)/total_velocity for semitone in midi_data.get_chroma()]

# Shift all notes up by 5 semitones
#Shiftキーすべてが5つの半音アップノート
for instrument in midi_data.instruments:
    # Don't want to shift drum notes
    #ドラムのノートをシフトしたくない
    if not instrument.is_drum:
        for note in instrument.notes:
            note.pitch += 5
# Synthesize the resulting MIDI data using sine waves
# 正弦波を使用して結果のMIDIデータを合成する
audio_data = midi_data.synthesize()




################################################################
#
# シンプルなMIDIファイルを作成するための使用例：
#
################################################################

# Create a PrettyMIDI object
# MIDIを作る
cello_c_chord = pretty_midi.PrettyMIDI()

# Create an Instrument instance for a cello instrument
# チェロのインスタンスを作る
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)

# Iterate over note names, which will be converted to note number later
# 繰り返す使うので、['C5', 'E5', 'G5']に名前をつける。
for note_name in ['C5', 'E5', 'G5']:

    # Retrieve the MIDI note number for this note name
    #このノート名のMIDIノート番号を取得します。
    note_number = pretty_midi.note_name_to_number(note_name)

    # Create a Note instance, starting at 0s and ending at .5s
    note = pretty_midi.Note(velocity=100, pitch=note_number, start=0, end=.5)

    # Add it to our cello instrument
    cello.notes.append(note)

# Add the cello instrument to the PrettyMIDI object
cello_c_chord.instruments.append(cello)

# Write out the MIDI data
cello_c_chord.write('cello-C-chord.mid')










