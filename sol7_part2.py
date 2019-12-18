from intcode_exp import IntCode
import sys

state = list(eval(open(sys.argv[1]).read()))

outp = 0
fperm = None

import itertools

for perm in list(itertools.permutations([5,6,7,8,9])):
		amps = [IntCode() for _ in range(5)]
		mode = 'init'
		start = 0
		i = 0
		while 1:

				if mode == 'init':
						phase = perm[i] 
						start = amps[i].compute(state.copy(), inputs=[phase, start])
				else:
						interm = amps[i%5].compute(inputs=[start])

						if amps[i%5].status != 'halted':
								start = interm
		
				i+=1

				if i==len(perm):
						mode = 'amping'

				if False not in [amp.status == 'halted' for amp in amps]:
						if start>outp:
								outp = start
								fperm = perm
						break


print(outp, fperm)
