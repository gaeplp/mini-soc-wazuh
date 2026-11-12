import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


RACINE = Path(__file__).resolve().parents[1]
SCRIPT = RACINE / "src" / "alertes_sqlite.py"
DONNEES = RACINE / "sample-data" / "alertes-demo.jsonl"


class TestAlertesSQLite(unittest.TestCase):
    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)
        self.base = Path(self.dossier.name) / "alertes.db"

    def lancer(self, *arguments):
        resultat = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "--db", str(self.base), *map(str, arguments)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        return resultat.stdout.strip()

    def test_import_sans_doublons(self):
        self.assertEqual(self.lancer("importer", DONNEES), "3 alerte(s) ajoutée(s).")
        self.assertEqual(self.lancer("importer", DONNEES), "0 alerte(s) ajoutée(s).")

    def test_chronologie_et_filtre_agent(self):
        self.lancer("importer", DONNEES)
        lignes = self.lancer("lister", "--agent", "demo-linux").splitlines()

        self.assertEqual(len(lignes), 3)
        self.assertIn("règle 5760", lignes[0])
        self.assertIn("règle 5715", lignes[1])
        self.assertIn("règle 554", lignes[2])
        self.assertEqual(self.lancer("lister", "--agent", "agent-inconnu"), "")

    def test_import_format_wazuh(self):
        donnees_wazuh = RACINE / "sample-data" / "alerte-wazuh-fictive.jsonl"

        self.assertEqual(
            self.lancer("importer", donnees_wazuh),
            "1 alerte(s) ajoutée(s).",
        )
        self.assertEqual(
            self.lancer("importer", donnees_wazuh),
            "0 alerte(s) ajoutée(s).",
        )

        resultat = self.lancer("lister", "--agent", "demo-linux")
        self.assertIn("règle 5760 | niveau 5 | Échec SSH fictif", resultat)

    def test_resume_par_regle(self):
        self.lancer("importer", DONNEES)
        donnees_wazuh = RACINE / "sample-data" / "alerte-wazuh-fictive.jsonl"
        self.lancer("importer", donnees_wazuh)

        self.assertEqual(
            self.lancer("resumer").splitlines(),
            [
                "Règle 554 : 1 alerte(s)",
                "Règle 5715 : 1 alerte(s)",
                "Règle 5760 : 2 alerte(s)",
            ],
        )

if __name__ == "__main__":
    unittest.main()
