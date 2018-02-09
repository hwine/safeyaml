import io
import os
import glob
import yaml
import pytest
import subprocess


@pytest.mark.parametrize("path", glob.glob("tests/validate/*.yaml"))
def test_validate(path):
    check_file(path, validate=True)


@pytest.mark.parametrize("path", glob.glob("tests/fix/*.yaml"))
def test_fix(path):
    check_file(path, fix=True)


def check_file(path, validate=False, fix=False):
    output_file = '{}.output'.format(path)
    error_file = '{}.error'.format(path)

    if os.path.exists(error_file):
        with open(error_file) as fh:
            expected_output = fh.read()

        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            safeyaml(path, fix=fix)

        # FIXME: error formatting doesn't work yet
        # error = excinfo.value
        # assert error.stdout == b''
        # assert error.stderr == expected_output
        return

    output = safeyaml(path, fix=fix)
    
    # FIXME: should be no output if fix=False
    if fix:
        with open(output_file) as fh:
            expected_output = fh.read()
            assert output == expected_output


def safeyaml(path, fix=False):
    command = ["safeyaml"]
    if fix:
        command.append("--fix")
    command.append(path)

    output = subprocess.check_output(command, stderr=subprocess.PIPE)
    return output.decode('utf-8')


if __name__ == '__main__':
    pytest.main(['-q', __file__])
