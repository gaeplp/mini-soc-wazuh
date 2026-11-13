import json
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

    def test_resume_filtre_deux_agents(self):
        self.lancer("importer", DONNEES)

        fichier_autre_agent = Path(self.dossier.name) / "autre-agent.jsonl"
        fichier_autre_agent.write_text(
            json.dumps({
                "timestamp": "2026-01-01T10:10:00Z",
                "agent": "autre-agent",
                "rule_id": 5760,
                "level": 5,
                "description": "Échec fictif sur un autre agent",
            }, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self.lancer("importer", fichier_autre_agent)

        self.assertEqual(
            self.lancer("resumer", "--agent", "autre-agent"),
            "Règle 5760 : 1 alerte(s)",
        )
        self.assertEqual(
            self.lancer("resumer", "--agent", "demo-linux").splitlines(),
            [
                "Règle 554 : 1 alerte(s)",
                "Règle 5715 : 1 alerte(s)",
                "Règle 5760 : 1 alerte(s)",
            ],
        )
        self.assertIn("Règle 5760 : 2 alerte(s)", self.lancer("resumer"))

    def test_sequences_ssh(self):
        fichier = Path(self.dossier.name) / "sequences-ssh.jsonl"

        evenements = [
            ("2026-11-06T08:16:50.000+0000", "lab-linux", 5715),  # trop tôt
            ("2026-11-06T08:17:25.986+0000", "lab-linux", 5760),
            ("2026-11-06T08:18:01.998+0000", "lab-linux", 5715),
            ("2026-11-06T08:58:08.743+0000", "lab-linux", 5760),
            ("2026-11-06T08:58:10.000+0000", "autre-agent", 5715),
            ("2026-11-06T08:58:14.746+0000", "lab-linux", 5715),
            ("2026-11-06T09:00:00.000+0000", "lab-linux", 5760),
            ("2026-11-06T09:02:00.000+0000", "lab-linux", 5715),  # trop tard
        ]

        alertes = [
            {
                "timestamp": horodatage,
                "agent": agent,
                "rule_id": regle,
                "level": 5 if regle == 5760 else 3,
                "description": "Événement SSH fictif",
            }
            for horodatage, agent, regle in evenements
        ]
        fichier.write_text(
            "\n".join(json.dumps(alerte, ensure_ascii=False) for alerte in alertes)
            + "\n",
            encoding="utf-8",
        )

        self.lancer("importer", fichier)
        lignes = self.lancer("sequences-ssh", "--agent", "lab-linux").splitlines()

        self.assertEqual(len(lignes), 2)
        self.assertIn("08:17:25.986", lignes[0])
        self.assertIn("08:18:01.998", lignes[0])
        self.assertIn("08:58:08.743", lignes[1])
        self.assertIn("08:58:14.746", lignes[1])

    def test_ids_wazuh_distincts(self):
        fichier = Path(self.dossier.name) / "ids-distincts.jsonl"
        alertes = [
            {
                "id": identifiant,
                "timestamp": "2026-01-01T12:00:00.000+0000",
                "agent": {"name": "demo-linux"},
                "rule": {
                    "id": "5760",
                    "level": 5,
                    "description": "Échec SSH fictif",
                },
            }
            for identifiant in ("evenement-001", "evenement-002")
        ]
        fichier.write_text(
            "\n".join(json.dumps(alerte, ensure_ascii=False) for alerte in alertes)
            + "\n",
            encoding="utf-8",
        )

        self.assertEqual(self.lancer("importer", fichier), "2 alerte(s) ajoutée(s).")
        self.assertEqual(self.lancer("importer", fichier), "0 alerte(s) ajoutée(s).")
        self.assertEqual(
            self.lancer("resumer", "--agent", "demo-linux"),
            "Règle 5760 : 2 alerte(s)",
        )

if __name__ == "__main__":
    unittest.main()
