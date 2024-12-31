from dataclasses import dataclass
import aoc
import re

@dataclass
class Gate:
    a: str
    b: str
    operator: str
    output: str

    def __hash__(self):
        return hash((self.a, self.b, self.operator, self.output))

def main(lines: list):
    wires = {}
    gates = []
    gates_with_input = {}

    pattern = r"(?P<a>.+) (?P<operator>XOR|OR|AND) (?P<b>.+) -> (?P<output>.+)"

    on_wire_section = True
    for line in lines:
        if line == "":
            on_wire_section = False
        elif on_wire_section:
            k, v = line.split(": ")
            wires[k] = (v == "1")
        else:
            parsed = re.match(pattern, line)
            a = parsed["a"]
            b = parsed["b"]
            gate = Gate(a, b, parsed["operator"], parsed["output"])
            gates.append(gate)
            if a not in gates_with_input:
                gates_with_input[a] = []
            gates_with_input.get(a).append(gate)
            if b not in gates_with_input:
                gates_with_input[b] = []
            gates_with_input.get(b).append(gate)
    
    while True:
        found_incomplete = False
        for gate in gates:
            if gate.a in wires and gate.b in wires and gate.output not in wires:
                found_incomplete = True
                if gate.operator == "AND":
                    wires[gate.output] = wires[gate.a] and wires[gate.b]
                elif gate.operator == "OR":
                    wires[gate.output] = wires[gate.a] or wires[gate.b]
                elif gate.operator == "XOR":
                    wires[gate.output] = wires[gate.a] != wires[gate.b]
        if not found_incomplete:
            break
    part1 = int(''.join(str(int(i)) for i in list(map(lambda key: wires[key], sorted(filter(lambda key: key[0] == "z", wires.keys()), reverse=True)))), 2)
    
    swapped_output_wires = set()
    while True:
        result = find_outputs_to_swap(wires, gates, gates_with_input)
        if not result:
            break
        swapped_output_wires.update(result)
    part2 = ",".join(sorted(list(swapped_output_wires)))

    return part1, part2

def find_outputs_to_swap(wires, gates, gates_with_input) -> tuple[str, str]:
    _, gates_to_check = find_gates_with_incorrect_output(wires, gates, gates_with_input)
    for gate_a in gates_to_check:
        for gate_b in gates_to_check:
            if gate_a == gate_b:
                continue
            temp = gate_a.output
            gate_a.output = gate_b.output
            gate_b.output = temp

            test_correct_gates, _ = find_gates_with_incorrect_output(wires, gates, gates_with_input)
            if gate_a in test_correct_gates and gate_b in test_correct_gates:
                return gate_a.output, gate_b.output
            else:
                temp = gate_a.output
                gate_a.output = gate_b.output
                gate_b.output = temp
    return None

def find_gates_with_incorrect_output(wires, gates, gates_with_input) -> tuple[list[Gate], list[Gate]]:
    correct_gates = set()
    input_wire_count = len(list(filter(lambda wire: wire[0] == "x", wires)))
    carry_gate = None
    for i in range(input_wire_count):
        x = "x" + str(i).rjust(2, "0")
        y = "y" + str(i).rjust(2, "0")
        z = "z" + str(i).rjust(2, "0")
        z_next = "z" + str(i+1).rjust(2, "0")

        if True:
            xor_gate = filter_gates(gates_with_input.get(x), "XOR")
            and_gate = filter_gates(gates_with_input.get(x), "AND")
            
            if i == 0:
                if xor_gate.output == z:
                    correct_gates.add(xor_gate)
                carry_gate = and_gate
            elif i == input_wire_count - 1:
                if carry_gate.output == z_next:
                    correct_gates.add(carry_gate)
            else:
                second_xor_gate = filter_gates(gates_with_input.get(xor_gate.output), "XOR")
                second_and_gate = filter_gates(gates_with_input.get(xor_gate.output), "AND")
                if second_xor_gate and second_and_gate:
                    correct_gates.add(xor_gate)
                    if carry_gate and gates_with_input.get(carry_gate.output) and second_xor_gate in gates_with_input.get(carry_gate.output) and second_and_gate in gates_with_input.get(carry_gate.output):
                        correct_gates.add(carry_gate)
                    if second_xor_gate.output == z:
                        correct_gates.add(second_xor_gate)
                    g1 = filter_gates(gates_with_input.get(and_gate.output), "OR")
                    g2 = filter_gates(gates_with_input.get(second_and_gate.output), "OR")
                    if g1 == g2:
                        correct_gates.add(and_gate)
                        correct_gates.add(second_and_gate)
                        carry_gate = g1
    gates_to_check = []
    for gate in gates:
        if gate not in correct_gates:
            gates_to_check.append(gate)
    return correct_gates, gates_to_check

def filter_gates(gates, operator) -> Gate:
    if gates:
        for gate in gates:
            if gate.operator == operator:
                return gate
    return None

aoc.run_lines(main, "day24.txt")
