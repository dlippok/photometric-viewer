import io as python_io
import unittest

from photometric_viewer.utils.ioutil import read_non_empty_line

WINDOWS_NEWLINE = "\r\n"
UNIX_NEWLINE = "\n"

class TestReadNonEmptyLine(unittest.TestCase):
    def test_no_empty_lines(self):
        lines_given = ["a", "b", "c"]
        lines_expected = ["a", "b", "c"]

        cases = [
            ("Windows encoding", WINDOWS_NEWLINE.join(lines_given)),
            ("Unix encoding", UNIX_NEWLINE.join(lines_given)),
        ]
        for case in cases:
            with(self.subTest(case=case[0])):
                f = python_io.StringIO(case[1])
                for expected_line in lines_expected:
                    self.assertEqual(read_non_empty_line(f), expected_line)

    def test_empty_lines_in_the_beginning(self):
        lines_given = ["", "a", "b", "c"]
        lines_expected = ["a", "b", "c"]

        cases = [
            ("Windows encoding", WINDOWS_NEWLINE.join(lines_given)),
            ("Unix encoding", UNIX_NEWLINE.join(lines_given)),
        ]
        for case in cases:
            with(self.subTest(case=case[0])):
                f = python_io.StringIO(case[1])
                for expected_line in lines_expected:
                    self.assertEqual(read_non_empty_line(f), expected_line)

    def test_empty_lines_in_the_end(self):
        lines_given = ["a", "b", "c", ""]
        lines_expected = ["a", "b", "c"]

        cases = [
            ("Windows encoding", WINDOWS_NEWLINE.join(lines_given)),
            ("Unix encoding", UNIX_NEWLINE.join(lines_given)),
        ]
        for case in cases:
            with(self.subTest(case=case[0])):
                f = python_io.StringIO(case[1])
                for expected_line in lines_expected:
                    self.assertEqual(read_non_empty_line(f), expected_line)

    def test_empty_between_content(self):
        lines_given = ["a", "", "b", "", "c"]
        lines_expected = ["a", "b", "c"]

        cases = [
            ("Windows encoding", WINDOWS_NEWLINE.join(lines_given)),
            ("Unix encoding", UNIX_NEWLINE.join(lines_given)),
        ]
        for case in cases:
            with(self.subTest(case=case[0])):
                f = python_io.StringIO(case[1])
                for expected_line in lines_expected:
                    self.assertEqual(read_non_empty_line(f), expected_line)