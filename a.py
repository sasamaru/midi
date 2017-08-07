import random
from numpy.random import *

# i12 = [1,2,3,4,5,6,7,8,9,10,11,12]


# def a(i):
# 	print("-------")
# 	print(i)
# 	print("--")
# 	for j in i12:
# 		print(j)
# 		p= (((i)/12)**j)*(1-((i-1)/12))
# 		print(p*100//0.1/10)

# for i in i12:
# 	a(i)

# import pretty_midi
# 12ずつ更新
# print(pretty_midi.note_name_to_number('A5'))
# print(pretty_midi.note_name_to_number('A4'))
# print(pretty_midi.note_name_to_number('A3'))
# print(pretty_midi.note_name_to_number('A2'))

# print(pretty_midi.note_name_to_number('B5'))
# print(pretty_midi.note_name_to_number('B4'))
# print(pretty_midi.note_name_to_number('B3'))
# print(pretty_midi.note_name_to_number('B2'))
x = poisson(1, 30)
print(x)
