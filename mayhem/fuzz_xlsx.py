#!/usr/bin/env python3
import atheris
import sys
import fuzz_helpers
import io
from contextlib import contextmanager


with atheris.instrument_imports():
    from xlsx2csv import Xlsx2csv

from xlsx2csv import InvalidXlsxFileException

@contextmanager
def nostdout():
    save_stdout = sys.stdout
    save_stderr = sys.stderr
    sys.stdout = io.BytesIO()
    sys.stderr = io.BytesIO()
    yield
    sys.stdout = save_stdout
    sys.stderr = save_stderr

ctr = 0

def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    global ctr
    ctr += 1
    with nostdout():
        try:
            with fdp.ConsumeTemporaryFile(suffix='.xlsx', as_bytes=True) as f:
                Xlsx2csv(f).convert('/dev/null')
        except InvalidXlsxFileException:
            return -1
        except TypeError:
            if ctr > 1:
                raise
            return -1
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
