import unittest

from hj212_parser import HJ212Parser


def make_message(data: str) -> str:
    parser = HJ212Parser()
    crc = f"{parser._crc16_ansi(data.encode('ascii')):04X}"
    return f"##{len(data.encode('ascii')):04d}{data}{crc}\r\n"


class HJ212ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = HJ212Parser()
        self.message = make_message(
            "QN=20261007170000000;ST=32;CN=2011;CP=&&DataTime=20261007170000&"
            "w01001-Rtd=12.3,w01001-Flag=N&&"
        )

    def test_validation_and_crc(self):
        self.assertTrue(self.parser.is_valid_message(self.message))
        self.assertTrue(self.parser.validate_crc(self.message))
        self.assertFalse(self.parser.is_valid_message(self.message[:-6] + "0000\r\n"))

    def test_parse_and_extract(self):
        fields = self.parser.parse_data_segment(self.message)
        self.assertEqual(fields["ST"], "32")
        values = self.parser.extract_monitoring_data(self.message)
        self.assertEqual(values["DataTime"], "20261007170000")
        self.assertEqual(values["w01001-Rtd"], "12.3")

    def test_length_and_terminator(self):
        self.assertFalse(self.parser.is_valid_message(self.message.replace("\r\n", "\n")))


if __name__ == "__main__":
    unittest.main()
