import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _ux_wire
import _fn189_rollout
import _fn189_custom_patch


class GenerationSafetyTests(unittest.TestCase):
    def test_custom_wiring_refuses_unverified_business_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / 'sample.html'
            original = '<html><body><input id="input"><button onclick="calc()">Go</button><div id="result"></div><script>\nfunction calc(){document.getElementById("result").textContent="⚠ valid warning";}</script></body></html>'
            page.write_text(original, encoding='utf-8')
            self.assertEqual(_ux_wire.apply_custom(str(page)), 'skip:business-verdict-required')
            self.assertEqual(page.read_text(encoding='utf-8'), original)

    def test_standard_rollout_rejects_unverified_verdict(self):
        with self.assertRaisesRegex(ValueError, 'business verdict'):
            _fn189_rollout.load_template()
        with self.assertRaisesRegex(ValueError, 'business verdict'):
            _fn189_rollout.build_standard('', {}, '', '', 'sample')

    def test_custom_rollout_rejects_unverified_verdict(self):
        with self.assertRaisesRegex(ValueError, 'business verdict'):
            _fn189_custom_patch.build_custom('', {}, '', 'sample')


if __name__ == '__main__':
    unittest.main()
