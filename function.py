# coding: UTF-8
import random
from numpy.random import *
import pretty_midi
import numpy as np

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

# 休符はx、引き伸ばしは-で表す。
MAJOR_RHYTHM_LIST =[[2,1,1],[1,1,1,1,"-"],[1,1,1,1],[2,1,1],[4],[2,2],[2,"x","x"],[4,"-"],["x","x",2] ]
MINOR_RHYTHM_LIST =[["x",1,1,1,"-"],[2,1,1],[1,1,2],["x",1,1,1],[2,2,"-"],[3,1],[3,1,"-"],[1,"x",1,1],[1,2,1,"-"],[2,"x",1],[1,1,1,"x"],["x",1,1,1,"-"],["x","x",1,1]]

# リズムパターンの中から使用するパターンをランダムに14個選択し、リストとして返す。
def making_use_rhythm_list():
	np.random.shuffle(MINOR_RHYTHM_LIST)
	return MAJOR_RHYTHM_LIST+MINOR_RHYTHM_LIST[:5]

# 小節数を受け取り、リズムリストを作る。返り値：[1,1,2,3,..,"x",2]など
def making_full_rythom(number_of_bar):
	result_rhythm = []
	rhythm_list = making_use_rhythm_list()
	list_length = len(rhythm_list)
	num=0
	prev_rhythm=0
	is_prev_tie=False
	while num<number_of_bar*2:#リストは1/2小節なので*2
		rand = np.random.randint(0,list_length-1)
		rhythm = rhythm_list[rand]
		for r in rhythm:
			if r=="-":
				is_prev_tie=True
			else:
				if (is_prev_tie)&(r!="x"):
					del result_rhythm[-1]
					rr = r
					r = prev_rhythm+rr
					is_prev_rhythm = rr
				elif r=="x":
					prev_rhythm=0
				else:
					prev_rhythm=r
				is_prev_tie=False
				result_rhythm.append(r)
		num+=1
	return result_rhythm
	

# リズムリストとコード進行を受け取って、(リズム, コード)のリストを返す。返り値：[(1,CHORD_C),(2,CHORD_C)..]
def match_rhythm_and_chord(rhythm_list, chord_progression):
	result_list = []
	total_rhythm = 0
	next_chord_number = 0
	for rhythm in rhythm_list:
		result_list.append((rhythm, chord_progression[next_chord_number]))
		if rhythm=="x":
			total_rhythm+=1
		else:
			total_rhythm+=rhythm
		next_chord_number=total_rhythm//8
	return result_list

# (リズム, コード)のリストを受け取り、(音程、リズム、コード)のリストを返す。
# まず、８分音符以外のコードに、自身の長さと前のコードからの距離をもとに楽譜を割り当てる。
def give_tone_to_rhythm1(rhythm_chord_list):
	result_list = []
	length_from_prevtone = 0
	prevtone = "0"
	probability_of_change = 0
	for rhythm_chord in rhythm_chord_list:
		rhythm = rhythm_chord[0]
		chord = rhythm_chord[1]
		if (rhythm==1)|(rhythm=="x"):
			length_from_prevtone+=1
			result_list.append(("0",rhythm, chord))
		else:
			tone = making_tone_from_prob_and_prevtone(prevtone, rhythm, length_from_prevtone, chord)
			length_from_prevtone = 0
			prevtone = tone
			result_list.append((chord[0], rhythm_chord[0], chord))
	return result_list

# (音程、リズム、コード)のリストを受け取り、(音程、リズム、コード)のリストを返す。
# 間の8部音符を埋めて行く。
def give_tone_to_rhythm2(tone_rhythm_chord_list):
	result_list = []
	prevtone = "C4"
	for trc in tone_rhythm_chord_list:
		if trc[1]=="x":
			prev_tone = 0
			result_list.append(trc)
		elif trc[1]!=1:
			prev_tone = pretty_midi.note_name_to_number(trc[0])
			result_list.append(trc)
		else:
			# ここを訂正。前後のコードから割り出す
			result_list.append(("0" , "x", trc[2]))
			# result_list.append((prevtone ,trc[1], trc[2]))
	return result_list

# 外音が連続した場合消す。
# def give_tone_to_rhythm3(tone_rhythm_chord_list):


# (音程、リズム、コード)のリストを受け取り、(音程、リズム)のリストを返す。
def make_music_from_3list(tone_rhythm_chord_list):
	result_list = []
	for l in tone_rhythm_chord_list:
		result_list.append((l[0], l[1]))
	return result_list

# 前の音符までの距離と、音符の長さから、前回の音符とのズレを返す。
def caliculate_tone_difference(length, tone_length):
	y = ((length/2)+tone_length)
	x = poisson(y, 1)
	# if x>12:
	# 	x=12
	return x

# コードと音符を受け取り、一番近い内音のintに変更する。
# (chord, int) -> int
def change_to_inner_tone(chord, tone):
	most_near = [100, "x"]
	num = [-12, 12, 0]
	for c in chord:
		for n in num:
			c_num = pretty_midi.note_name_to_number(c)+n
			if abs(c_num-tone)<=(most_near[0]):
				most_near = [abs(c_num-tone), c_num]
	return most_near[1]


# (一つ前の音程, 音の変わりやすさ, コード)を受け取り、音程を返す
# 12で一つの周期となる。
# なので、飛ぶ値は最大値で12に設定する。
# 引数のprevとlengthでは、合わせて12まで行くように重みを設定
def making_tone_from_prob_and_prevtone(prev, tone_length, length, chord):
	diff = caliculate_tone_difference(length, tone_length)
	new_tone = "0"
	if prev == "0":
		new_tone = chord[0]
		new_tone = pretty_midi.note_name_to_number(new_tone)
		prev = new_tone
	else:
		prev = pretty_midi.note_name_to_number(prev)
		# 50%で音程が上下する
		if np.random.randint(0,1)==1:
			new_tone = prev+diff
		else:
			new_tone = prev-diff
	# 2: 50%で内音, 3:75%, 4:100%で内音に
	# if tone_length < np.random.randint(1, 4):
	# 	new_tone = change_to_inner_tone(chord ,new_tone)
	new_tone = pretty_midi.note_number_to_name(new_tone)
	return new_tone





	

#########引用############################################
#########引用############################################
#########引用############################################

# 引数の楽器に（音程, 開始時間, 長さ）の音符をつける。
def add_tone_to_instrument(tone, start_position, length, instrument):
	    note_number = pretty_midi.note_name_to_number(tone)
	    print([tone,note_number])
	    note = pretty_midi.Note(velocity=100, pitch=note_number, start=start_position, end=(start_position+length))
	    instrument.notes.append(note)


#########引用############################################
#########引用############################################
#########引用############################################



def add_music_to_instrument(music, instrument):
	start_position=0
	for m in music:
		tone=m[0]
		length=m[1]
		if length=="x":
			length=1*BASE_NOTE_LENGTH
		else:
			length = m[1]*BASE_NOTE_LENGTH
			add_tone_to_instrument(tone, start_position, length, instrument)
		start_position+=length


#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
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
		rand = np.random.randint(0,5)
		chord_progression.append(chord_list[rand])
		num+=1
	return chord_progression

# 1小節分のリズムを生成。floatの配列を返す。
def making_one_bar_rhythm():
	rhythm = []
	total_rhythm_length = 0
	while total_rhythm_length*BASE_NOTE_LENGTH<ONE_BAR_LENGTH:
		note_length = np.random.randint(1,4)
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
			sound = innner_sound[np.random.randint(0,len(innner_sound)-1)]
		else:
			# sound = TONE_LIST[np.random.randint(0,len(TONE_LIST)-1)]
			sound = use_tone_list[np.random.randint(0,len(use_tone_list)-1)]
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






#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################





#					main
#____________________________________________#

CANON_CHORD = [CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G, CHORD_C, CHORD_G, CHORD_Am, CHORD_Em, CHORD_F, CHORD_G]
chord_progression = CANON_CHORD
test_rhythm = making_full_rythom(42)

test_r_and_c = match_rhythm_and_chord(test_rhythm,chord_progression)
print(test_r_and_c)
print("")
print("")
print("")
main_music1 = give_tone_to_rhythm1(test_r_and_c)
print(main_music1)
print("")
print("")
print("")
main_music2 = give_tone_to_rhythm2(main_music1)
print(main_music2)
print("")
print("")
print("")
main_music = make_music_from_3list(main_music2)
print(main_music)

add_music_to_instrument(main_music, flute)

add_chord_progression_to_instrument(chord_progression ,cello)
midi.instruments.append(cello)
midi.instruments.append(flute)
midi.write('making/chord_test.mid')


