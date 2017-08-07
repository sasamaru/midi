#既存のファイルの呼び出しの関係についての練習。
import pretty_midi

midi_data = pretty_midi.PrettyMIDI('making/level_up.mid')

# 楽器のデータの取得は、
# MIDIから楽器の配列を取得
## midi_data.instruments
# 楽器からNoteの配列を取得
## instrument.notes
# でできるみたい。
for instrument in midi_data.instruments:
    if not instrument.is_drum:
        for note in instrument.notes:
        	#どうやら, pretty_midi.Noteのインスタンスnoteについて
			#note.pitchで音程を変更できるようだ。
            note.pitch -= 5

midi_data.write('making/level_up2.mid')