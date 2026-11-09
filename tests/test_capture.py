import io, unittest
from host.ccd_capture import read_capture, write_frame

class CaptureTests(unittest.TestCase):
    def test_synthetic_roundtrip(self):
        f = {"timestamp_us": 7, "data": bytes([0x10, 0x20]), "synthetic": True}
        got = list(read_capture(io.StringIO(write_frame(f))))[0]
        self.assertEqual(got["data"], f["data"])
        self.assertTrue(got["synthetic"])

    def test_malformed_hex_fails(self):
        with self.assertRaises(ValueError):
            list(read_capture(io.StringIO('{"type":"frame","timestamp_us":0,"data":"gg"}')))

if __name__ == "__main__": unittest.main()
