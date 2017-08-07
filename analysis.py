# coding: UTF-8
import pretty_midi
import math

musics = ["melt", "rolling_girl", "shinkai", "wim", "fflower", "howareyou", "brs", "mozaiku", "senbonzakura", "pandahero", "setsunatrip"]
musics2 = ["kagayake", "fuwa", "listen", "hotti", "pure", "ui", "angel"]
musics3 = ["WelcomeToTheJapariPark"]
# musics = pretty_midi.PrettyMIDI('msk/'+music+'.mid')
# musics = ["TomorrowNeverKnows"]


def get_variance(musics):
	for music in musics:
		# MIDIファイルを読み込む
		midi_data = pretty_midi.PrettyMIDI(music)
		# # 楽器の一覧
		instrument = midi_data.instruments
		average = 0
		variance = 0
		print(music)
		for i in instrument:
			notes = i.notes
			note_sum = 0
			note_sum2 = 0
			for note in notes:
				note_sum+=note.pitch
			average = note_sum/len(notes)
			for note in notes:
				note_sum2+=note.pitch*note.pitch
			variance = math.sqrt((note_sum2/len(notes))-average*average)
			print("分散(符号区別なし)："+str(variance))
		for i in instrument:
			notes = i.notes
			note_sum = 0
			note_sum2 = 0
			length = 0
			total_length = 0
			for note in notes:
				length = note.end-note.start
				note_sum+=note.pitch*length
				total_length+=length
			average = note_sum/total_length
			for note in notes:
				length = note.end - note.start
				note_sum2+=note.pitch*note.pitch*length
			variance = math.sqrt((note_sum2/total_length)-average*average)

		print("-----")
		print("分散："+str(variance))
		print("____________________________-")



# 曲から短い音をとる
def get_long_tone(musics):
	for music in musics:
		print(music)
		midi_data = pretty_midi.PrettyMIDI('msk/'+music+'.mid')
		instrument = midi_data.instruments

		midi = pretty_midi.PrettyMIDI(initial_tempo=midi_data.estimate_tempo())#

		for i in instrument:
			
			cello_program = pretty_midi.instrument_name_to_program('Cello')#
			cello = pretty_midi.Instrument(program=cello_program)#
			cello1 = pretty_midi.Instrument(program=cello_program)#
			cello2 = pretty_midi.Instrument(program=cello_program)#

			notes = i.notes
			result_list = []
			for note in notes:
				length = note.end - note.start
				length = length // 0.0001
				if length not in result_list:
					result_list.append(length)
			min_length = min(result_list)
			result_list.remove(min_length)
			if result_list!=[]:
				second_min_length = min(result_list)
			else:
				second_min_length = 0
			for note in notes:
				length = note.end - note.start
				length = length // 0.0001
				cello.notes.append(note)
				if length!=min_length:
					cello1.notes.append(note)
					if second_min_length!=0&(length!=second_min_length):
						cello2.notes.append(note)

			midi.instruments.append(cello)#
			midi.instruments.append(cello1)#
			midi.instruments.append(cello2)#

		midi.write('msk/change/'+music+'.mid')

# キーを引数だけあげる（下げる）
def get_long_tone(music, up):
	print(music)
	midi_data = pretty_midi.PrettyMIDI('msk/'+music+'.mid')
	instrument = midi_data.instruments

	midi = pretty_midi.PrettyMIDI(initial_tempo=midi_data.estimate_tempo())#

	for i in instrument:
		
		cello_program = pretty_midi.instrument_name_to_program('Cello')
		cello = pretty_midi.Instrument(program=cello_program)
		cello2 = pretty_midi.Instrument(program=cello_program)
		notes = i.notes
		for note in notes:
			# print(note)
			# cello.notes.append(note)
			note.pitch += up
			# print(note)
			cello2.notes.append(note)
		# midi.instruments.append(cello)
		midi.instruments.append(cello2)
	midi.write('msk/change_key/'+music+'.mid')

get_long_tone("WelcomeToTheJapariPark", 9)










