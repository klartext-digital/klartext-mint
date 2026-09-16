"""Regression checks for the user's explicit hold on the production launch."""
import unittest
from release_policy import PREVIEW_URL, validate_preview


class PreviewPolicyTest(unittest.TestCase):
    def setUp(self):
        self.config = dict(base_url=PREVIEW_URL, indexable=False, approved_paths=[])

    def test_approved_preview(self):
        validate_preview(self.config)

    def test_production_domain_rejected_even_when_noindex(self):
        self.config['base_url'] = 'https://klartext-digital.ch/'
        with self.assertRaises(ValueError):
            validate_preview(self.config)

    def test_indexing_cannot_be_enabled(self):
        for value in [True, 'false', None, 0]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_preview({**self.config, 'indexable': value})

    def test_path_allowlist_cannot_be_enabled(self):
        self.config['approved_paths'] = ['seo/']
        with self.assertRaises(ValueError):
            validate_preview(self.config)

    def test_missing_settings_fail_closed(self):
        for key in self.config:
            incomplete = {k: v for k, v in self.config.items() if k != key}
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    validate_preview(incomplete)


if __name__ == '__main__':
    unittest.main()
