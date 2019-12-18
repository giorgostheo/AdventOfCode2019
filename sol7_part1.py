from intcode_exp import IntCode
import sys

state = list(eval(open(sys.argv[1]).read()))
inputs = list(map(int, open(sys.argv[2]).read()[:-1].split(',')))

outp = 0
fperm = None

import itertools

for perm in list(itertools.permutations([0,1,2,3,4])):
		start = 0
		for phase in perm:

				start = IntCode().compute(state, inputs=[phase, start])
		
		if start>outp:
				outp = start
				fperm = perm

print(outp, fperm)
