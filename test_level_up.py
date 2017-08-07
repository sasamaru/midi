# coding: UTF-8

import pretty_midi
# Create a PrettyMIDI object
# MIDIを作る
cello_c_chord = pretty_midi.PrettyMIDI(initial_tempo=200.0)

# Create an Instrument instance for a cello instrument
# チェロのインスタンスを作る
cello_program = pretty_midi.instrument_name_to_program('Cello')
cello = pretty_midi.Instrument(program=cello_program)
cello2 = pretty_midi.Instrument(program=cello_program)

# Iterate over note names, which will be converted to note number later
so='G6'
fa='F6'
mib='D#6'

do='C6'
si='B5'
sib='A#5'
ra='A5'

so_n = pretty_midi.note_name_to_number(so)
fa_n = pretty_midi.note_name_to_number(fa)
mib_n = pretty_midi.note_name_to_number(mib)

do_n = pretty_midi.note_name_to_number(do)
si_n = pretty_midi.note_name_to_number(si)
sib_n = pretty_midi.note_name_to_number(sib)
ra_n = pretty_midi.note_name_to_number(ra)


# Create a Note instance, starting at 0s and ending at .5s
# ここで、音符の設定。 start~endまでを、pitchの音程で再生する。
# pitchはint,floatで、周波数的な何か？ これを使わず、note_name_to_numberを使うのが良さそう。
note = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*0, end=0.6*0.25)
note2 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*0.25, end=0.6*0.5)
note3 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*0.5, end=0.6*0.75)
note4 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*0.75, end=0.6*1)
note5 = pretty_midi.Note(velocity=110, pitch=mib_n, start=0.6*1.25, end=0.6*1.5)
note6 = pretty_midi.Note(velocity=110, pitch=so_n, start=0.6*1.75, end=0.6*2)
note7 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*2.25, end=0.6*2.5)
note8 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*2.5, end=0.6*3)
note9 = pretty_midi.Note(velocity=110, pitch=fa_n, start=0.6*3, end=0.6*4)

note11 = pretty_midi.Note(velocity=110, pitch=do_n, start=0.6*0, end=0.6*0.25)
note12 = pretty_midi.Note(velocity=110, pitch=si_n, start=0.6*0.25, end=0.6*0.5)
note13 = pretty_midi.Note(velocity=110, pitch=sib_n, start=0.6*0.5, end=0.6*0.75)
note14 = pretty_midi.Note(velocity=110, pitch=ra_n, start=0.6*0.75, end=0.6*1)
note15 = pretty_midi.Note(velocity=110, pitch=ra_n, start=0.6*1.25, end=0.6*1.5)
note16 = pretty_midi.Note(velocity=110, pitch=si_n, start=0.6*1.75, end=0.6*2)
note17 = pretty_midi.Note(velocity=110, pitch=ra_n, start=0.6*2.25, end=0.6*2.5)
note18 = pretty_midi.Note(velocity=110, pitch=ra_n, start=0.6*2.5, end=0.6*3)
note19 = pretty_midi.Note(velocity=110, pitch=ra_n, start=0.6*3, end=0.6*4)

# Add it to our cello instrument
# 音符を各楽器に割り当てる。
cello.notes.append(note)
cello.notes.append(note2)
cello.notes.append(note3)
cello.notes.append(note4)
cello.notes.append(note5)
cello.notes.append(note6)
cello.notes.append(note7)
cello.notes.append(note8)
cello.notes.append(note9)
cello2.notes.append(note11)
cello2.notes.append(note12)
cello2.notes.append(note13)
cello2.notes.append(note14)
cello2.notes.append(note15)
cello2.notes.append(note16)
cello2.notes.append(note17)
cello2.notes.append(note18)
cello2.notes.append(note19)

# Add the cello instrument to the PrettyMIDI object
#これで、楽器を追加する。上の作業ではまだ楽器がmidiの演奏内に追加されていない。
cello_c_chord.instruments.append(cello)
cello_c_chord.instruments.append(cello2)


# Write out the MIDI data
cello_c_chord.write('making/level_up.mid')