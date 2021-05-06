import pathlib as pl
from unittest import TestCase
import unittest
from file_saver import FileSaver


class TestCaseBase(TestCase):
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))


class ActualTest(TestCaseBase):
    def test_file_saving(self):
        Fs = FileSaver()
        res = Fs.save_file("test.json", b"abc")

        path = pl.Path("data_dump/test.json")
        self.assertIsFile(path)




if __name__ == '__main__':
    unittest.main()
