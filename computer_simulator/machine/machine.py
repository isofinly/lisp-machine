from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from computer_simulator.isa import Arg, ArgType, Instruction, Opcode
from computer_simulator.machine.hardwire import ControlUnit, DataPath, Port

MEMORY_SIZE: int = 2048


@dataclass
class BinaryProgram:
    memory: list[Instruction | int]


def read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


def read_input(file_path: str) -> list[int]:
    with open(file_path, encoding="utf-8") as file:
        file_str = file.read()
        return [ord(c) for c in file_str]


def read_program(file_path: str) -> BinaryProgram:
    binary_data = Path(file_path).read_bytes()
    memory: list[Instruction | int] = [0 for _ in range(MEMORY_SIZE)]
    address = 0

    for i in range(0, len(binary_data), 8):
        # logging.debug(f"bin: {(binary_data[i:i + 4]).hex()} {(binary_data[i + 4:i + 8]).hex()}")
        instruction_word = int.from_bytes(binary_data[i : i + 4], "big")
        arg_value = int.from_bytes(binary_data[i + 4 : i + 8], "big")

        opcode_value = instruction_word >> 24
        addressing_type_value = (instruction_word >> 22) & 0b11

        opcode = next((op for op in Opcode if int(op.binary, 2) == opcode_value), None)
        if opcode is None:
            raise ValueError(str(opcode_value) + "Unknown opcode")

        addressing_type = {
            0b00: ArgType.DIRECT,
            0b01: ArgType.ADDRESS,
            0b10: ArgType.INDIRECT,
            0b11: ArgType.STACK_OFFSET,
        }[addressing_type_value]

        if opcode in {Opcode.JMP, Opcode.CALL}:
            arg = Arg(arg_value, ArgType.ADDRESS)
        elif opcode in {Opcode.PUSH, Opcode.OUT, Opcode.POP, Opcode.HLT, Opcode.IN}:
            arg = None
        else:
            arg = Arg(arg_value, addressing_type)

        memory[address] = Instruction(opcode, arg)
        # logging.debug(f"Loaded instruction at address {address}: {memory[address]}")

        if address == 0:
            address = 512
        else:
            address += 1

    return BinaryProgram(memory)


def simulation(program: BinaryProgram, limit: int, program_input: list[int]) -> tuple[list[int], int, int]:
    data_path = DataPath(program.memory, {Port.IN.name: program_input, Port.OUT.name: []})
    control_unit = ControlUnit(data_path)

    logging.debug("%s", control_unit)
    while not control_unit.halted and control_unit.tick_n < limit:
        control_unit.tick()

    return data_path.ports[Port.OUT.name], control_unit.executed_instruction_n, control_unit.tick_n


def main(code: str, input_file: str) -> None:
    program = read_program(code)
    program_input = read_input(input_file)

    result = simulation(program, limit=1_000_000, program_input=program_input)

    print("".join([chr(c) for c in result[0]]))
    print(f"instructions_n: {result[1]} ticks: {result[2]}")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    assert len(sys.argv) >= 3, f"Usage: python3 {Path(__file__).name} <code> <input>"
    main(sys.argv[1], sys.argv[2])
