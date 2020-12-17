from unittest import TestCase

from file_saver import FileSaver



class Test_Scorer(TestCase):

    def test_file_saving(self):
        Fs = FileSaver()
        res = Fs.save_file("test.json",b"abc")
        self.assertEqual(target_url, res.url)


if __name__ == '__main__':
    unittest.main()
