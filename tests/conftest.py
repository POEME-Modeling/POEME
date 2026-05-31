# tests/conftest.py
import pytest
from pathlib import Path


@pytest.fixture
def data_dir():
    return Path(__file__).parent / "data"


def test_print_output(capsys, data_dir):
    # my_function()  # this prints something
    captured = capsys.readouterr()  # grab what was printed
    expected = (data_dir / "expected_output.txt").read_text()
    assert captured.err == ""
    assert captured.out == expected


# def test_text_output(data_dir):
#     result = my_function()
#     expected = (data_dir / "real_t_expected.txt").read_text()
#     assert result == expected


def compare_file_out(result_file, ref_file):
    result = result_file.read_text()
    expected = ref_file.read_text()
    assert result == expected


def compare_pop_out(ref_file):
    pop_file = Path(__file__).parent / "pop.out"
    return compare_file_out(pop_file, ref_file)


def compare_pretty_out(ref_file):
    pop_file = Path(__file__).parent / "pretty.out"
    return compare_file_out(pop_file, ref_file)


def run_tests():
    pytest.main([__file__])
