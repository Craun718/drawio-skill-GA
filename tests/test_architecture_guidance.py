#!/usr/bin/env python3
"""Regression tests for architecture diagram guidance."""

import json
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "drawio-skill", "SKILL.md")
DIAGRAM_TYPES = os.path.join(
    ROOT, "skills", "drawio-skill", "references", "diagram-types.md"
)
XML_AUTHORING = os.path.join(
    ROOT, "skills", "drawio-skill", "references", "xml-authoring.md"
)
STYLE_PRESETS = os.path.join(
    ROOT, "skills", "drawio-skill", "references", "style-presets.md"
)
DEFAULT_PRESET = os.path.join(
    ROOT, "skills", "drawio-skill", "styles", "built-in", "default.json"
)


class TestArchitectureGuidance(unittest.TestCase):
    def read(self, path):
        with open(path, encoding="utf-8") as fh:
            return fh.read()

    def test_project_architecture_pattern_is_present(self):
        skill = self.read(SKILL)
        for marker in (
            "Project / Program Architecture",
            "proposal-style project/program architecture",
        ):
            self.assertIn(marker, skill)

        diagram_types = self.read(DIAGRAM_TYPES)
        for marker in (
            "Project / Program Architecture",
            "current systems",
            "target platform",
            "data exchange",
            "do not assume a fixed set of section titles",
        ):
            self.assertIn(marker, diagram_types)

        xml = self.read(XML_AUTHORING)
        for marker in (
            "Project Architecture style",
            "proposal-style project/program architecture",
            "do not assume a fixed set of section titles",
        ):
            self.assertIn(marker, xml)
        self.assertIn('parent="containerId"', xml)
        self.assertIn("coordinates relative to their `parent`", xml)
        self.assertIn("`&#xa;`", xml)

    def test_project_architecture_guidance_preserves_source_fidelity(self):
        for path in (SKILL, DIAGRAM_TYPES, XML_AUTHORING):
            self.assertIn("proposal", self.read(path))
        self.assertIn("Preserve proposal wording verbatim", self.read(SKILL))
        self.assertIn(
            "Keep the proposal's exact wording and punctuation",
            self.read(DIAGRAM_TYPES),
        )
        self.assertIn("preserve exact proposal wording", self.read(XML_AUTHORING))

    def test_capability_stack_pattern_is_present(self):
        text = self.read(DIAGRAM_TYPES)
        for marker in (
            "Capability Stack Architecture",
            "aggregate component",
            "subordinate components",
            "right rail",
            "tiered semantic palette",
        ):
            self.assertIn(marker, text)
        self.assertIn("Do not turn subordinate components into separate steps", text)
        self.assertIn(
            "Do not add a legend merely because the diagram uses a tiered semantic palette",
            text,
        )

    def test_xml_authoring_references_the_pattern(self):
        text = self.read(XML_AUTHORING)
        self.assertIn("Capability Stack Architecture", text)
        self.assertIn("Aggregate component full-width", text)

    def test_tiered_palette_exception_is_consistent(self):
        for path in (SKILL, DIAGRAM_TYPES, XML_AUTHORING, STYLE_PRESETS):
            self.assertIn("tiered semantic palette", self.read(path))

    def test_color_restraint_is_theme_based_not_hex_based(self):
        for path in (SKILL, DIAGRAM_TYPES, XML_AUTHORING, STYLE_PRESETS):
            text = self.read(path)
            self.assertIn("at most three theme colors", text)
            self.assertIn("tints", text)
            self.assertIn("shades", text)
            self.assertNotIn("at most three chromatic colors", text)
            self.assertNotIn("at most three soft chromatic colors", text)

    def test_v2_architecture_defaults_are_bundled(self):
        with open(DEFAULT_PRESET, encoding="utf-8") as fh:
            preset = json.load(fh)
        self.assertEqual(preset["font"]["fontSize"], 19)
        self.assertEqual(preset["font"]["titleFontSize"], 20)
        self.assertIn("strokeWidth=3", preset["edges"]["style"])
        self.assertIn("fontSize=18", preset["edges"]["style"])


if __name__ == "__main__":
    unittest.main()
