import binascii
import contextlib
import io
import logging
import os
import tempfile
import typing

import pytest
from computer_simulator.machine import machine
from computer_simulator.translator import translator


@pytest.mark.golden_test("../golden/*.yml")
def test_whole_by_golden(golden: typing.Any, caplog: typing.Any) -> None:
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source")
        input_stream = os.path.join(tmpdirname, "input")
        target = os.path.join(tmpdirname, "target")
        debug_output = os.path.join("debug.txt")

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["source"])
        with open(input_stream, "w", encoding="utf-8") as file:
            file.write(golden["input"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(source, target)
            print("============================================================")
            machine.main(target, input_stream)

        with open(target, "rb") as file:
            code = file.read()

        with open(debug_output, encoding="utf-8") as file:
            debug_content = file.read()

        expected_code = binascii.unhexlify(golden["code"].strip())
        expected_debug = golden["debug"]

        assert code == expected_code, f"{code.hex()} != {expected_code.hex()}"
        assert stdout.getvalue() == golden["output"]
        assert caplog.text.strip() == golden["log"].strip()
        assert debug_content.strip() == expected_debug.strip()
