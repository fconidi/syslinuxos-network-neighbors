import unittest

from i18n import CATALOGS, choose_language, tr


class LanguageTests(unittest.TestCase):
    def test_five_complete_languages(self):
        self.assertEqual(set(CATALOGS), {"en", "it", "fr", "de", "es"})
        english = set(CATALOGS["en"])
        for catalog in CATALOGS.values():
            self.assertEqual(set(catalog), english)
            self.assertTrue(all(catalog.values()))

    def test_locale_selection(self):
        self.assertEqual(choose_language({"LANG": "fr_CA.UTF-8"}), "fr")
        self.assertEqual(choose_language({"LC_ALL": "C", "LANG": "it_IT.UTF-8"}), "en")
        self.assertEqual(choose_language({"LC_ALL": "C.UTF-8", "LANGUAGE": "it"}), "en")
        self.assertEqual(choose_language({"LANG": "pt_BR.UTF-8"}), "en")
        self.assertEqual(choose_language({"LANGUAGE": "de:en", "LANG": "en_US.UTF-8"}), "de")
        self.assertEqual(tr("it", "refresh"), "Aggiorna")


if __name__ == "__main__":
    unittest.main()
