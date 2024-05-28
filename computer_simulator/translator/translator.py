from __future__ import annotations

import re
import sys
from pathlib import Path

from computer_simulator.isa import Instruction
from computer_simulator.translator.expression_translator import Program, translate_program
from computer_simulator.translator.tokenizer import Token, tokenize


def run_translator(tokens: list[Token]) -> Program:
    program = Program()
    translate_program(tokens, program)
    return program


def read_file(filename: str) -> str:
    return Path(filename).read_text(encoding="utf-8")


def preprocess(source: str) -> str:
    regex = re.compile(r'\(include\s+"(.+)"\)')
    match = regex.search(source)
    while match:
        file = match.group(1)
        source = source.replace(match.group(), read_file(file))
        match = regex.search(source)
    return source


def main(source: str, target: str) -> None:
    with open(target, "wb") as f:
        source_code = read_file(source)
        preprocessed_code = preprocess(source_code)
        tokenized_code = tokenize(preprocessed_code)
        program = run_translator(tokenized_code)

        print(
            f"source LoC: {len(source_code.split('\n'))} code instr: {len([x for x in program.memory if isinstance(x, Instruction)])}"
        )
        f.write(program.to_machine_code())
        if len(sys.argv) > 2:
            write_debug_output(program, sys.argv[2] + ".debug.txt")
        else:
            write_debug_output(program, "debug.txt")


def write_debug_output(program: Program, debug_file_path: str) -> None:
    with open(debug_file_path, "w") as debug_file:
        for address, instruction in enumerate(program.memory):
            if isinstance(instruction, Instruction):
                hex_code = f"{int(instruction.opcode.binary, 2):02X}"
                if instruction.arg:
                    hex_code += f"{instruction.arg.value:016X}"
                else:
                    hex_code += "0000000000000000"
                mnemonic = f"{instruction.opcode.mnemonic} {instruction.arg if instruction.arg else ''}"
                debug_file.write(f"{address:04X} - {hex_code} - {mnemonic}\n")


if __name__ == "__main__":
    assert len(sys.argv) == 3, f"Usage: python3 {Path(__file__).name} <source> <target>"
    main(sys.argv[1], sys.argv[2])
