import numpy as np
import sys

class IntCode(object):
		def __init__(self, anchor=0):
				self.anchor = anchor
				self.version = 'v1.1'
				self.status = 'active'
				self.state = None
				self.rel_base = 0

		def print_all(self):
				print('5tate ->', self.state)
				print('Inputs ->', self.inputs)
				print('Anchor ->', self.anchor)
				print('Version ->', self.version)


		def _get_instruction(self):
				return self.state[self.anchor]


		def _get_opcode_and_params(self, instruction):
				return str(instruction).zfill(5)[-2:], str(instruction).zfill(5)[:-2]

		def _assign(self, inpt, param, offset):
			if param == '0':
					self.state[self.state[self.anchor+offset]] = inpt
			elif param == '2':
					self.state[self.state[self.anchor+offset]+self.rel_base] = inpt
			else:
					print('shit')


		def _get_values(self, opcode, params):

				p_verb = params[-2]
				p_noun = params[-1]

				if p_noun == '0':
						noun = self.state[self.state[self.anchor+1]]
				elif p_noun =='1':

						noun = self.state[self.anchor+1]
				elif p_noun == '2':
						noun = self.state[self.state[self.anchor+1]+self.rel_base]
				if opcode != '04' and opcode != '09':
						if p_verb == '0':
								verb = self.state[self.state[self.anchor+2]]
						elif p_verb =='1':
								verb = self.state[self.anchor+2]
						elif p_verb == '2':
								verb = self.state[self.state[self.anchor+2]+self.rel_base]
				else:
						verb = None

				return noun, verb


		def _run_for_opcode(self, opcode, params):

				if opcode == '01':
						self._assign(sum(self._get_values(opcode, params)), params[0], offset=3)
						self.anchor += 4

				if opcode == '02':
						self._assign(np.prod(self._get_values(opcode, params)), params[0], offset=3)

						self.anchor += 4

				if opcode == '03':
						self._assign(self.inputs.pop(0), params[-1], offset=1)
						self.anchor += 2

				if opcode == '04':
						self.outputs.append(self._get_values(opcode, params)[0])
						self.anchor += 2

				if opcode == '05':
						noun, verb = self._get_values(opcode, params)
						if noun != 0:
								self.anchor = verb
						else:
								self.anchor += 3

				if opcode == '06':
						noun, verb = self._get_values(opcode, params)
						if noun == 0:
								self.anchor = verb
						else:
								self.anchor += 3

				if opcode == '07':
						noun, verb = self._get_values(opcode, params)
						if noun < verb:
								self._assign(1, params[0], offset=3)
						else:
								self._assign(0, params[0], offset=3)
						self.anchor += 4

				if opcode == '08':
						noun, verb = self._get_values(opcode, params)
						if noun == verb:
								self._assign(1, params[0], offset=3)
						else:
								self._assign(0, params[0], offset=3)
						self.anchor += 4

				if opcode == '09':
						noun, verb = self._get_values(opcode, params)
						self.rel_base += noun
						self.anchor += 2



		def compute(self, state=None, inputs=None, verbose=True, pause_on_output=False):
				if state is not None: self.state = state
				if self.status == 'paused': self.status = 'active'
				self.inputs = inputs
				self.outputs = []
				while 1:
						instruction = self._get_instruction()
						if verbose: print('Instruction: ', instruction)
						if str(instruction)[-2:] == '99':
								self.status = 'halted'
								return
						opcode, params = self._get_opcode_and_params(instruction)
						if verbose: print('Opcode: ', opcode, '\nParams', params)
						self._run_for_opcode(opcode, params)
						if self.outputs and pause_on_output:
								self.status='paused'
								return self.outputs[0]


def test_build(test_file = 'tests.npy'):
	data = np.load(test_file, allow_pickle=True)
	for ind, (state, inps, ans) in enumerate(data):
		v1 = IntCode()
		v1.compute(state, inputs=inps)
		if v1.outputs[0] == ans:
			print(f'[+] Test {ind} successful')
		else:
			print(f'[-] Test {ind} failed. Expected {ans}, got {v1.outputs}')


def sim(state, inputs, verbose=False):
	v1 = IntCode()
	v1.compute(state, inputs=inputs, verbose=verbose)
	print('Results: ', v1.outputs)
	#print('Info : ', v1.print_all())


if __name__=='__main__':
	if sys.argv[1] == '-1':
		test_build()
		sys.exit()
	print('Args: ', sys.argv)
	state = list(eval(open(sys.argv[1]).read()))
	print(len(state))
	if sys.argv[3] == '-1':
			state.extend([0]*len(state)*10)
	print(len(state))
	inputs = list(map(int, open(sys.argv[2]).read()[:-1].split(',')))
	sim(state, inputs)
