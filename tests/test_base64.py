import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bin"))  # noqa


from b64 import decode_base64


class TestB64Command(unittest.TestCase):
    def test_decode_simple_ascii(self):
        self.assertEqual(decode_base64("ZnJlZA==").decode("utf-8"), "fred")
        self.assertEqual(decode_base64("TXkgRmFuY3kgQkFTRTY0IFRlWFQ="), b"My Fancy BASE64 TeXT")

    def test_padding_fix(self):

        self.assertEqual(decode_base64("V2VsY29tZQ=="), b"Welcome")  # Correct
        self.assertEqual(decode_base64("V2VsY29tZQ="), b"Welcome")
        self.assertEqual(decode_base64("V2VsY29tZQ"), b"Welcome")
        self.assertEqual(decode_base64("V2VsY29tZQ==="), b"Welcome")  # Ignore extras

    def test_fixing_utf16le(self):
        self.assertEqual(decode_base64("fAAgAGUAdgBhAGwAIABzAGUAc").decode("utf-16le"),
                         "| eval se")


if __name__ == '__main__':
    unittest.main()
