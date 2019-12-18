import numpy as np
import sys

class IntCode(object):
    def __init__(self, anchor=0):
        self.anchor = anchor        
        self.inputs = []
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
    
        
    def _get_values(self):
        p_verb = self.params[0]
        p_noun = self.params[1]
        
        if p_noun == '0':
            self.noun = self.state[self.state[self.anchor+1]]
        elif p_noun =='1':
            
            self.noun = self.state[self.anchor+1]
        if self.opcode != '04':
            if p_verb == '0':
                self.verb = self.state[self.state[self.anchor+2]]
            elif p_verb =='1':
                self.verb = self.state[self.anchor+2]
        else:
            self.verb = None

        
            

    def _update_anchor(self):
        if self.opcode == '01':
            self.anchor += 4
            
        if self.opcode == '02':
            self.anchor += 4
            
        if self.opcode == '03':
            self.anchor += 2
            
        if self.opcode == '04':
            self.anchor += 2
            
        if self.opcode == '05':
            if self.noun != 0:
                self.anchor = self.verb
            else:    
                self.anchor += 3
                
        if self.opcode == '06':
            if self.noun == 0:
                self.anchor = self.verb
            else:    
                self.anchor += 3
                
        if self.opcode == '07':
            self.anchor += 4
            
        if self.opcode == '08':
            self.anchor += 4
            
    
    def _opcode_1(self):
        self._get_values()
        self.state[self.state[self.anchor+3]] = self.noun+self.verb
#         self.update_anchor()

    def _opcode_2(self):
        self._get_values()
        self.state[self.state[self.anchor+3]] = self.noun*self.verb

    def _opcode_3(self):
        self.state[self.state[self.anchor+1]] = self.inputs.pop(0)
        
    def _opcode_4(self):
        self._get_values()
        self.output = self.noun
        
    def _opcode_5(self):
        self._get_values()
        
    def _opcode_6(self):
        self._get_values()
        
    def _opcode_7(self):
        self._get_values()
        if self.noun < self.verb:
            self.state[self.state[self.anchor+3]] = 1
        else:
            self.state[self.state[self.anchor+3]] = 0
    
    def _opcode_8(self):
        self._get_values()
        if self.noun == self.verb:
            self.state[self.state[self.anchor+3]] = 1
        else:
            self.state[self.state[self.anchor+3]] = 0
    
    def _run_for_opcode(self, opcode):
        if self.opcode == '01':
            self._opcode_1()
            
        if self.opcode == '02':
            self._opcode_2()
            
        if self.opcode == '03':
            self._opcode_3()
            
        if self.opcode == '04':
            self._opcode_4()
            
        if self.opcode == '05':
            self._opcode_5()
            
        if self.opcode == '06':
            self._opcode_6()
            
        if self.opcode == '07':
            self._opcode_7()
            
        if self.opcode == '08':
            self._opcode_8()
            
            
    def compute(self, state=None, inputs=None, verbose=False):
        if state is not None: self.state = state
        self.inputs = inputs
        while 1:
            instruction = self._get_instruction()
            if verbose: print('Instruction: ', instruction)
            if instruction == 99:
                return np.nan
            opcode, params = self._get_opcode_and_params(instruction)
            if verbose: print('Opcode: ', opcode, '\nParams', params)
            self._run_for_opcode()
            if verbose: print('Noun: ', self.noun, '\nVerb: ', self.verb)
            self._update_anchor()
            if self.output is not None:
                return self.output
    

def test_build(test_file = 'tests.npy'):
	data = np.load(test_file, allow_pickle=True)
	for ind, (state, inps, ans) in enumerate(data):
		v1 = IntCode()
		v1.compute(state, inputs=inps)
		if v1.output == ans:
			print(f'[+] Test {ind} successful')
		else:
			print(f'[-] Test {ind} failed')    
    
        
def sim(state, inputs, verbose=False):
	v1 = IntCode()
	v1.compute(state, inputs=inputs, verbose=verbose)
	print('Results: ', v1.output)
	print('Info : ', v1.print_all())


if __name__=='__main__':
	if sys.argv[1] == '-1':
		test_build()
		sys.exit()
	print('Args: ', sys.argv)
	state = list(eval(open(sys.argv[1]).read()))
	inputs = list(map(int, open(sys.argv[2]).read()[:-1].split(',')))
	sim(state, inputs)

