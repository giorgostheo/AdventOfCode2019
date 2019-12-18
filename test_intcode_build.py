import itertools,sys
from intcode import IntCode
import numpy as np

print('Testing inputs 3 and 5...')
test_file = 'testing_inputs/tests.npy'
data = np.load(test_file, allow_pickle=True)
for ind, (state, inps, ans) in enumerate(data):
	v1 = IntCode()
	v1.compute(state, inputs=inps)
	if v1.outputs[0] == ans:
		print(f'[+] (3,5) Test {ind} successful')
	else:
		print(f'[-] (3,5) Test {ind} failed. Expected {ans}, got {v1.outputs}')

print('Testing input 7...')

state = list(eval(open('testing_inputs/input7.txt').read()))

outp = 0
fperm = None


for perm in list(itertools.permutations([0,1,2,3,4])):
		start = 0
		for phase in perm:

				start = IntCode().compute(state.copy(), inputs=[phase, start])

		if start>outp:
				outp = start
				fperm = perm

if outp == 24405:
    print(f'[+] (7) Test 1 successful')
else:
    print(f'[-] (7)) Test 1 failed. Expected {ans}, got {outp}')


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


if outp == 8271623:
    print(f'[+] (7) Test 2 successful')
else:
    print(f'[-] (7)) Test 2 failed. Expected {ans}, got {outp}')
