# coding: UTF-8

import pretty_midi
import random

# チェロのインスタンスを作る
midi = pretty_midi.PrettyMIDI(initial_tempo=200.0)
cello_program = pretty_midi.instrument_name_to_program('Cello')
flute_program = pretty_midi.instrument_name_to_program('Flute')
cello = pretty_midi.Instrument(program=cello_program)
flute = pretty_midi.Instrument(program=flute_program)

# 音程の定義
C3 = 'C3'
C4 = 'C4' 
C5 = 'C5' 
C6 = 'C6'
D3 = 'D3'
D4 = 'D4' 
D5 = 'D5' 
D6 = 'D6'
E3 = 'E3'
E4 = 'E4' 
E5 = 'E5' 
E6 = 'E6'
F3 = 'F3'
F4 = 'F4' 
F5 = 'F5' 
F6 = 'F6'
G3 = 'G3'
G4 = 'G4' 
G5 = 'G5' 
G6 = 'G6'
A3 = 'A3'
A4 = 'A4' 
A5 = 'A5' 
A6 = 'A6'
B3 = 'B3'
B4 = 'B4' 
B5 = 'B5' 
B6 = 'B6'

# コードの定義
CHORD_C = [C4, E4, G4]
CHORD_Dm = [D4, F4, A4]
CHORD_Em = [E4, G4, B4]
CHORD_F = [F4, A4, C5]
CHORD_G = [G4, B4, D5]
CHORD_Am = [A4, C5, E5]

DIATONIC_CODE_C = [CHORD_C, CHORD_Dm, CHORD_Em, CHORD_F, CHORD_G, CHORD_Am]
TONE_LIST = [G4, A4, B4, C5, D5, E5, F5, G5, A5, B5, C6, D6, E6, F6, G6]

# 8分音符を基本単位とする. 今の所、1小節を1としている
BASE_NOTE_LENGTH = 0.125
ONE_BAR_LENGTH = BASE_NOTE_LENGTH*8

#					function
#____________________________________________#

# コードを受け取って、内音と外音を取得する。返り値：(内音stringlist, 外音stringlist)
def get_inner_outer_sound(chord):
	if chord==CHORD_C:
		innner_sound=[C5, C6, E5, E6, G4, G5, G6]
		innner_sound=[C5, E5, G5]
		outer_sound=[G4, A4, B4, C5, D5, E5, F5, G5, A5]
	elif chord==CHORD_Dm:
		innner_sound=[D5, D6, F5, F6, A4, A5]
		innner_sound=[D5, F5, A5]
		outer_sound=[A4, B4, C5, D5, E5, F5, G5, A5, B5]
	elif chord==CHORD_Em:
		innner_sound=[E5, G5, B5]
		outer_sound=[B4, C5, D5, E5, F5, G5, A5, B5, C6]
	elif chord==CHORD_F:
		innner_sound=[F5, A5, C6]
		outer_sound=[C5, D5, E5, F5, G5, A5, B5, C6, D6]
	elif chord==CHORD_G:
		innner_sound=[G5, B5, D6]
		outer_sound=[D5, E5, F5, G5, A5, B5, C6, D6, E6]
	elif chord==CHORD_Am:
		innner_sound=[A5, C6, E6]
		outer_sound=[E5, F5, G5, A5, B5, C6, D6, E6, F6]
	# outer_set=set(TONE_LIST) - set(innner_sound)
	# outer_sound = list(outer_set)
	return (innner_sound, outer_sound)

# 引数の楽器に（コード, 開始時間, 長さ）の音符をつける。
def add_chord_to_instrument(chord, start_position, length, instrument):
	for note_name in chord:
	    note_number = pretty_midi.note_name_to_number(note_name)
	    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_position, end=(start_position+length))
	    instrument.notes.append(note)

# 引数の楽器に（音程, 開始時間, 長さ）の音符をつける。
def add_tone_to_instrument(tone, start_position, length, instrument):
	    note_number = pretty_midi.note_name_to_number(tone)
	    print([tone,note_number])
	    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_position, end=(start_position+length))
	    instrument.notes.append(note)

# コード進行と楽器を受け取り、楽器に割り当てる。
def add_chord_progression_to_instrument(chord_progression, instrument):
	num = 0
	for chord in chord_progression :
		add_chord_to_instrument(chord, num, 1, instrument)
		num+=1

# コードリストと、小節数を受け取り、コードを小節数だけ並べたコード進行リストを返す。
def making_chord_progression(chord_list, number_of_bar):
	chord_progression = []
	length = len(chord_list)-1
	num = 0
	rand = 0
	while num<number_of_bar:
		rand = random.randint(0,5)
		chord_progression.append(chord_list[rand])
		num+=1
	return chord_progression

# 1小節分のリズムを生成。floatの配列を返す。
def making_one_bar_rhythm():
	rhythm = []
	total_rhythm_length = 0
	while total_rhythm_length*BASE_NOTE_LENGTH<ONE_BAR_LENGTH:
		note_length = random.randint(1,4)
		if note_length > ONE_BAR_LENGTH/BASE_NOTE_LENGTH-total_rhythm_length:
			note_length = ONE_BAR_LENGTH/BASE_NOTE_LENGTH-total_rhythm_length
		total_rhythm_length+=note_length
		rhythm.append(note_length)
	return rhythm

# 1小節分のリズムとコードを受け取って、リズムに音程を割り当てたものを返す。返り値：(音階string、リズムfloat)のリスト
def give_rhythm_tone(chord, rhythm):
	tone_list = []
	prev_sound = ""
	innner_sound = get_inner_outer_sound(chord)[0]
	outer_sound = get_inner_outer_sound(chord)[1]
	#追加
	use_tone_list = list(set(innner_sound)&set(outer_sound))
	#ここまで
	for r in rhythm:
		if prev_sound in outer_sound:
			sound = innner_sound[random.randint(0,len(innner_sound)-1)]
		else:
			# sound = TONE_LIST[random.randint(0,len(TONE_LIST)-1)]
			sound = use_tone_list[random.randint(0,len(use_tone_list)-1)]
		prev_sound = sound
		tone_list.append((sound, r))
	return tone_list

# コード進行表と楽器を受け取って、メロディーを作成する。返り値：(音階string、リズムfloat)のリスト
def making_music(chord_progression):
	music = []
	for chord in chord_progression:
		rhythm = making_one_bar_rhythm()
		tone = give_rhythm_tone(chord, rhythm)
		music.append(tone)
	return music

# メロディー(音階string、リズムfloat)のリスト　と楽器を受け取り、楽器にメロディーを割り当てる
def add_music_to_instrument(music, instrument):
	start_position=0
	for music_per_var in music:
		for m in music_per_var:
			tone = m[0]
			length = m[1]*BASE_NOTE_LENGTH
			add_tone_to_instrument(tone, start_position, length, instrument)
			start_position += length

#					main
#____________________________________________#
CANON_CHORD = [CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G]
chord_progression = CANON_CHORD
# chord_progression = making_chord_progression(DIATONIC_CODE_C, 50)
add_chord_progression_to_instrument(chord_progression ,cello)
main_music = making_music(chord_progression)
print(main_music)
add_music_to_instrument(main_music, flute)
midi.instruments.append(cello)
midi.instruments.append(flute)
midi.write('making/chord_test.mid')

