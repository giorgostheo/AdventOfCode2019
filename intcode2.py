import numpy as np
import sys

class IntCode(object):
		def __init__(self, anchor=0):
				self.anchor = anchor				
				self.version = 'v1.1'
				self.status = 'active'
				self.state = None
				
		def print_all(self):
				print('5tate ->', self.state)
				print('Inputs ->', self.inputs)
				print('Anchor ->', self.anchor)
				print('Version ->', self.version)
				

		def _get_instruction(self):
				return self.state[self.anchor]
				

		def _get_opcode_and_params(self, instruction):
				return str(instruction).zfill(4)[-2:], str(instruction).zfill(4)[:-2]
		
				
		def _get_values(self, opcode, params):
				
				p_verb = params[0]
				p_noun = params[1]
				
				if p_noun == '0':
						noun = self.state[self.state[self.anchor+1]]
				elif p_noun =='1':
						
						noun = self.state[self.anchor+1]
				if opcode != '04':
						if p_verb == '0':
								verb = self.state[self.state[self.anchor+2]]
						elif p_verb =='1':
								verb = self.state[self.anchor+2]
				else:
						verb = None

				return noun, verb

						
		def _run_for_opcode(self, opcode, params):

				if opcode == '01':
						self.state[self.state[self.anchor+3]] = sum(self._get_values(opcode, params))
						self.anchor += 4
						
				if opcode == '02':
				
						self.state[self.state[self.anchor+3]] = np.prod(self._get_values(opcode, params))
						self.anchor += 4
						
				if opcode == '03':
						self.state[self.state[self.anchor+1]] = self.inputs.pop(0)
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
								self.state[self.state[self.anchor+3]] = 1
						else:
								self.state[self.state[self.anchor+3]] = 0
						self.anchor += 4
						
				if opcode == '08':
						noun, verb = self._get_values(opcode, params)
						if noun == verb:
								self.state[self.state[self.anchor+3]] = 1
						else:
								self.state[self.state[self.anchor+3]] = 0
						self.anchor += 4
						
						
		def compute(self, state=None, inputs=None, verbose=False, pause_on_output=True):
				if state is not None: self.state = state
				if self.status == 'paused': self.status = 'active'
				self.inputs = inputs
				self.outputs = []
				while 1:
						instruction = self._get_instruction()
						if verbose: print('Instruction: ', instruction)
						if instruction == 99:
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
	inputs = list(map(int, open(sys.argv[2]).read()[:-1].split(',')))
	sim(state, inputs)

