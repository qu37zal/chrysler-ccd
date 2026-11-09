import io, unittest
from host.ccd_capture import read_capture, write_frame
from host.multibus_capture import read_records

class CaptureTests(unittest.TestCase):
    def test_synthetic_roundtrip(self):
        f = {"timestamp_us": 7, "data": bytes([0x10, 0x20]), "synthetic": True}
        got = list(read_capture(io.StringIO(write_frame(f))))[0]
        self.assertEqual(got["data"], f["data"])
        self.assertTrue(got["synthetic"])

    def test_malformed_hex_fails(self):
        with self.assertRaises(ValueError):
            list(read_capture(io.StringIO('{"type":"frame","timestamp_us":0,"data":"gg"}')))

    def test_multibus_keeps_threads_and_synthetic_marker(self):
        source = '\n'.join([
            '{"type":"edge","thread":"ccd","timestamp_us":10,"level":true,"synthetic":true}',
            '{"type":"frame","thread":"sci_6","timestamp_us":11,"data":"a5","synthetic":true}',
        ])
        got = list(read_records(io.StringIO(source)))
        self.assertEqual([x["thread"] for x in got], ["ccd", "sci_6"])
        self.assertEqual(got[1]["data"], bytes([0xA5]))
        self.assertTrue(all(x["synthetic"] for x in got))

    def test_multibus_requires_thread_identity(self):
        with self.assertRaises(ValueError):
            list(read_records(io.StringIO('{"type":"edge","timestamp_us":0,"level":false}')))

if __name__ == "__main__": unittest.main()
