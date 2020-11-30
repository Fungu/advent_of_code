import io
import itertools
import sys
	
class Mode:
	def __init__(self, mode_code):
		if mode_code == 0:
			self.read = Mode.mem_read
			self.write = Mode.mem_write
		elif mode_code == 1:
			self.read = Mode.imm_read
		elif mode_code == 2:
			self.read = Mode.rel_read
			self.write = Mode.rel_write
		
	def mem_read(mem, addr):
		return mem[addr]
	
	def mem_write(mem, addr, val):
		mem[addr] = val
		
	def imm_read(mem, val):
		return val
		
	def rel_read(mem, addr):
		return mem[mem.rb + addr]
		
	def rel_write(mem, addr, val):
		mem[mem.rb + addr] = val
		

class Memory:
	def __init__(self, mem):
		self.mem = mem[:]
		self.rb = 0
	
	def read(self, addr, mode):
		return mode.read(self, addr)
		
	def write(self, addr, mode, value):
		mode.write(self, addr, value)
	
	def __setitem__(self, addr, value):
		self.expand_if_needed(addr)
		self.mem[addr] = value
	
	def __getitem__(self, addr):
		self.expand_if_needed(addr)
		return self.mem[addr]
		
	def expand_if_needed(self, addr):
		if isinstance(addr, slice):
			min_needed_len = addr.stop
		else:
			min_needed_len = addr + 1
		if min_needed_len > len(self.mem):
			self.mem += [0 for _ in range(len(self.mem), min_needed_len)]

class Instruction:
	def __init__(self, opcode, num_params, operation):
		self.opcode = opcode
		self.num_params = num_params
		self.operation = operation
		
	def execute(self, mem, ip, modes, ins, outs):
		return self.operation(mem, ip, modes, ins, outs)
	
	def decode(instruction_code):
		opcode = instruction_code % 100
		instruction = instructions[opcode]
		param_modes = []
		mode_code = instruction_code // 100
		for i in range(instruction.num_params):
			param_modes.append(Mode(mode_code % 10))
			mode_code //= 10
		return (instruction, param_modes)
		
	def err(mem, ip, modes, ins, outs):
		return (-1, ip)
		
	def add(mem, ip, modes, ins, outs):
		ix, jx, wx = mem[ip + 1:ip + 4]
		im, jm, wm = modes[0:3]
		mem.write(wx, wm, mem.read(ix, im) + mem.read(jx, jm))
		return (0, ip + 4)
		
	def mul(mem, ip, modes, ins, outs):
		ix, jx, wx = mem[ip + 1:ip + 4]
		im, jm, wm = modes[0:3]
		mem.write(wx, wm, mem.read(ix, im) * mem.read(jx, jm))
		return (0, ip + 4)
		
	def rd(mem, ip, modes, ins, outs):
		wx = mem[ip + 1]
		wm = modes[0]
		if len(ins) == 0:
			return (1, ip)
		mem.write(wx, wm, ins.pop(0))
		return (0, ip + 2)
		
	def wr(mem, ip, modes, ins, outs):
		ix = mem[ip + 1]
		im = modes[0]
		outs.append(mem.read(ix, im))
		return (0, ip + 2)
		
	def jnz(mem, ip, modes, ins, outs):
		cx, ax = mem[ip + 1:ip + 3]
		cm, am = modes[0:2]
		return (0, mem.read(ax, am) if mem.read(cx, cm) else ip + 3)
		
	def jz(mem, ip, modes, ins, outs):
		cx, ax = mem[ip + 1:ip + 3]
		cm, am = modes[0:2]
		return (0, mem.read(ax, am) if not mem.read(cx, cm) else ip + 3)
		
	def lt(mem, ip, modes, ins, outs):
		ix, jx, wx = mem[ip + 1:ip + 4]
		im, jm, wm = modes[0:3]
		mem.write(wx, wm, 1 if mem.read(ix, im) < mem.read(jx, jm) else 0)
		return (0, ip + 4)
		
	def eq(mem, ip, modes, ins, outs):
		ix, jx, wx = mem[ip + 1:ip + 4]
		im, jm, wm = modes[0:3]
		mem.write(wx, wm, 1 if mem.read(ix, im) == mem.read(jx, jm) else 0)
		return (0, ip + 4)
		
	def arb(mem, ip, modes, ins, outs):
		ix = mem[ip + 1]
		im = modes[0]
		mem.rb += mem.read(ix, im)
		return (0, ip + 2)
		
	def end(mem, ip, modes, ins, outs):
		return (2, ip)


instructions = [Instruction(i, 0, Instruction.err) for i in range(100)]
for i in [
	Instruction(1, 3, Instruction.add),
	Instruction(2, 3, Instruction.mul),
	Instruction(3, 1, Instruction.rd),
	Instruction(4, 1, Instruction.wr),
	Instruction(5, 2, Instruction.jnz),
	Instruction(6, 2, Instruction.jz),
	Instruction(7, 3, Instruction.lt),
	Instruction(8, 3, Instruction.eq),
	Instruction(9, 1, Instruction.arb),
	Instruction(99, 0, Instruction.end)
]:
	instructions[i.opcode] = i

class Intcode:
	def __init__(self, infile):
		code = infile.read()
		self.mem = [int(s) for s in code.split(',')]
	
class Process:
	def __init__(self, mem, in_pipe, out_pipe):
		self.mem = mem
		self.in_pipe = in_pipe
		self.out_pipe = out_pipe
		self.ip = 0
		self.state = 0
	
	def execute(self, yield_after=None):
		repeat_params = [None]
		if yield_after != None:
			repeat_params += [yield_after]
		for _ in itertools.repeat(*repeat_params):
			if self.state == 0 or self.state == 1 and len(self.in_pipe) > 0:
				instruction, modes = Instruction.decode(self.mem[self.ip])
				self.state, self.ip = instruction.execute(self.mem, self.ip, modes, self.in_pipe, self.out_pipe)
			else:
				break
		return self.state
		
	
class Kernel:
	def __init__(self, fairness = None):
		self.fairness = fairness
		self.processes = []
		self.next_pid = 0
		
	def execute(self, intcode, in_pipe, out_pipe):
		mem = Memory(intcode.mem)
		process = (self.next_pid, Process(mem, in_pipe, out_pipe))
		self.next_pid += 1
		self.processes.append(process)
		
	def __iter__(self):
		while len(self.processes) > 0:
			pid, process = self.processes.pop(0)
			state = process.execute(self.fairness)
			if state in [0, 1]:
				self.processes.append((pid, process))
			elif state < 0:
				p_mem = process.mem
				p_ip = process.ip
				p_ins = p_mem[p_ip]
				print("Error in process #{}: instruction {} at addess {} returned {}".format(pid, p_ins, p_ip, state))
#			elif state == 2:
#				print("Process #{} exited normally".format(pid))
			yield

with open("input/day9.txt") as infile:
	kernel = Kernel()
	program = Intcode(infile)
	in_pipe = [2]
	out_pipe = []
	kernel.execute(program, in_pipe, out_pipe)
	for _ in kernel:
		continue
	print("BOOST output: {}".format(out_pipe))