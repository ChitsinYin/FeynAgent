import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skills" / "feynagent" / "SKILL.md"


def _split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")

    try:
        frontmatter, body = text.split("\n---\n", 1)
    except ValueError as exc:
        raise AssertionError("SKILL.md must close YAML frontmatter") from exc

    return frontmatter.removeprefix("---\n"), body


class SkillMetadataTests(unittest.TestCase):
    def test_feynagent_skill_frontmatter_is_valid(self):
        text = SKILL_MD.read_text(encoding="utf-8")
        frontmatter, body = _split_frontmatter(text)

        metadata = yaml.safe_load(frontmatter)

        self.assertIsInstance(metadata, dict)
        self.assertEqual(metadata.get("name"), "feynagent")
        self.assertIsInstance(metadata.get("name"), str)
        self.assertIsInstance(metadata.get("description"), str)
        self.assertTrue(metadata["name"].strip())
        self.assertTrue(metadata["description"].strip())
        self.assertTrue(body.strip())


if __name__ == "__main__":
    unittest.main()
