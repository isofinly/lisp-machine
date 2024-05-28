from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Opcode(Enum):
    LD = ("LD", "00000")
    ST = ("ST", "00001")
    ADD = ("ADD", "00010")
    SUB = ("SUB", "00011")
    LT = ("LT", "00100")
    GT = ("GT", "00101")
    EQ = ("EQ", "00110")
    MOD = ("MOD", "00111")
    DIV = ("DIV", "01000")
    MUL = ("MUL", "01001")
    JZ = ("JZ", "01010")
    JNZ = ("JNZ", "01011")
    JMP = ("JMP", "01100")
    POP = ("POP", "01101")
    PUSH = ("PUSH", "01110")
    CALL = ("CALL", "01111")
    RET = ("RET", "10000")
    IN = ("IN", "10001")
    OUT = ("OUT", "10010")
    HLT = ("HLT", "10011")

    def __init__(self, mnemonic: str, binary: str):
        self.mnemonic = mnemonic
        self.binary = binary

    def __str__(self) -> str:
        return self.value[0]


class ArgType(Enum):
    DIRECT: str = "DIRECT"
    ADDRESS: str = "ADDRESS"
    INDIRECT: str = "INDIRECT"
    STACK_OFFSET: str = "STACK_OFFSET"

    def __str__(self) -> str:
        return self.value


@dataclass
class Arg:
    value: int | None
    arg_type: ArgType

    def __str__(self) -> str:
        return f"{self.value} ({self.arg_type})"


@dataclass
class Instruction:
    opcode: Opcode
    arg: Arg | None
    comment: str | None = None

    def __str__(self) -> str:
        r = f"{self.opcode}"
        if self.arg:
            r += f" arg[{self.arg}] "
        if self.comment:
            r += f" ({self.comment})"
        return f"Instr({r})"
