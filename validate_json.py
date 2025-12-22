#!/usr/bin/env python3
"""
Liturgische Analyse JSON Validator

Validates JSON files against the schema expected by docs/index.html.
Based on the structure of voorbeeld_01.json.

Usage:
    python validate_json.py <json_file>
    python validate_json.py docs/voorbeeld_02.json
"""

import json
import sys
from pathlib import Path
from typing import Any, Optional


class ValidationError:
    def __init__(self, path: str, message: str, severity: str = "error"):
        self.path = path
        self.message = message
        self.severity = severity  # "error", "warning", "info"

    def __str__(self):
        return f"[{self.severity.upper()}] {self.path}: {self.message}"


class LiturgischeAnalyseValidator:
    """Validator for Liturgische Analyse JSON files."""

    # Required top-level sections
    REQUIRED_SECTIONS = [
        '00_meta',
        '01_zondag_kerkelijk_jaar',
        '02_sociaal_maatschappelijke_context',
        '03_waardenorientatie',
        '04_geloofsorientatie',
        '05_interpretatieve_synthese',
        '06_actueel_wereldnieuws',
        '07_politieke_orientatie',
        '08_exegese',
        '09_kunst_cultuur',
        '10_focus_en_functie',
        '11_kalender',
        '12_representatieve_hoorders',
        '13_homiletische_analyse',
        '14_gebeden',
        '15_kindermoment',
        'Bijbelteksten'
    ]

    # Section-specific required keys
    SECTION_REQUIRED_KEYS = {
        '00_meta': ['plaatsnaam', 'gemeente', 'datum'],
        '01_zondag_kerkelijk_jaar': ['lezingen'],
        '08_exegese': ['per_lezing'],
        '10_focus_en_functie': ['opties'],
        '11_kalender': ['dagen'],
        '12_representatieve_hoorders': ['personas'],
        '14_gebeden': ['gebeden'],
        '15_kindermoment': ['kindermoment_opties'],
        'Bijbelteksten': ['grondtekst', 'nbv21', 'naardense_bijbel']
    }

    # Expected types for sections
    SECTION_TYPES = {
        '00_meta': dict,
        '01_zondag_kerkelijk_jaar': dict,
        '08_exegese': dict,
        '10_focus_en_functie': dict,
        '11_kalender': dict,
        '12_representatieve_hoorders': dict,
        '14_gebeden': dict,
        '15_kindermoment': dict,
        'Bijbelteksten': dict
    }

    def __init__(self):
        self.errors: list[ValidationError] = []
        self.data: Optional[dict] = None

    def validate_file(self, file_path: str) -> bool:
        """Validate a JSON file. Returns True if valid, False otherwise."""
        self.errors = []
        path = Path(file_path)

        # Check file exists
        if not path.exists():
            self.errors.append(ValidationError("", f"File not found: {file_path}"))
            return False

        # Parse JSON
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(ValidationError("", f"Invalid JSON: {e}"))
            return False
        except Exception as e:
            self.errors.append(ValidationError("", f"Error reading file: {e}"))
            return False

        # Check root is dict
        if not isinstance(self.data, dict):
            self.errors.append(ValidationError("", f"Root must be an object, got {type(self.data).__name__}"))
            return False

        # Validate structure
        self._validate_required_sections()
        self._validate_meta()
        self._validate_zondag_kerkelijk_jaar()
        self._validate_exegese()
        self._validate_focus_en_functie()
        self._validate_kalender()
        self._validate_hoorders()
        self._validate_gebeden()
        self._validate_kindermoment()
        self._validate_bijbelteksten()

        return len([e for e in self.errors if e.severity == "error"]) == 0

    def _validate_required_sections(self):
        """Check all required sections exist."""
        for section in self.REQUIRED_SECTIONS:
            if section not in self.data:
                self.errors.append(ValidationError(section, "Missing required section"))
            elif self.data[section] is None:
                self.errors.append(ValidationError(section, "Section is null"))

    def _check_required_keys(self, section: str, obj: dict, keys: list[str]):
        """Check required keys exist in an object."""
        for key in keys:
            if key not in obj:
                self.errors.append(ValidationError(f"{section}.{key}", "Missing required key"))
            elif obj[key] is None:
                self.errors.append(ValidationError(f"{section}.{key}", "Value is null", "warning"))

    def _check_type(self, path: str, value: Any, expected_type: type, allow_null: bool = False) -> bool:
        """Check value is of expected type."""
        if value is None:
            if not allow_null:
                self.errors.append(ValidationError(path, f"Expected {expected_type.__name__}, got null"))
            return allow_null
        if not isinstance(value, expected_type):
            self.errors.append(ValidationError(path, f"Expected {expected_type.__name__}, got {type(value).__name__}"))
            return False
        return True

    def _check_array_not_empty(self, path: str, arr: list) -> bool:
        """Check array is not empty."""
        if len(arr) == 0:
            self.errors.append(ValidationError(path, "Array is empty", "warning"))
            return False
        return True

    def _validate_meta(self):
        """Validate 00_meta section."""
        section = '00_meta'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        meta = self.data[section]
        self._check_required_keys(section, meta, ['plaatsnaam', 'gemeente', 'datum'])

        # Check types
        for key in ['plaatsnaam', 'gemeente', 'datum', 'adres', 'website']:
            if key in meta and meta[key] is not None:
                self._check_type(f"{section}.{key}", meta[key], str, allow_null=True)

    def _validate_zondag_kerkelijk_jaar(self):
        """Validate 01_zondag_kerkelijk_jaar section."""
        section = '01_zondag_kerkelijk_jaar'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['lezingen'])

        # Validate lezingen
        if 'lezingen' in data and isinstance(data['lezingen'], dict):
            lezingen = data['lezingen']
            expected_lezingen = ['eerste_lezing', 'psalm', 'epistel', 'evangelie']
            for lez in expected_lezingen:
                if lez not in lezingen:
                    self.errors.append(ValidationError(f"{section}.lezingen.{lez}", "Missing lezing", "warning"))
                elif lezingen[lez] is not None and isinstance(lezingen[lez], dict):
                    # Check lezing has referentie or boek+hoofdstuk
                    lez_data = lezingen[lez]
                    has_ref = 'referentie' in lez_data or ('boek' in lez_data and 'hoofdstuk' in lez_data)
                    if not has_ref:
                        self.errors.append(ValidationError(
                            f"{section}.lezingen.{lez}",
                            "Lezing should have 'referentie' or 'boek'+'hoofdstuk'",
                            "warning"
                        ))

    def _validate_exegese(self):
        """Validate 08_exegese section."""
        section = '08_exegese'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['per_lezing'])

        if 'per_lezing' in data:
            if not self._check_type(f"{section}.per_lezing", data['per_lezing'], list):
                return
            self._check_array_not_empty(f"{section}.per_lezing", data['per_lezing'])

            # Validate each lezing entry
            for i, lezing in enumerate(data['per_lezing']):
                path = f"{section}.per_lezing[{i}]"
                if not isinstance(lezing, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(lezing).__name__}"))
                    continue

                if 'referentie' not in lezing:
                    self.errors.append(ValidationError(f"{path}.referentie", "Missing referentie"))

    def _validate_focus_en_functie(self):
        """Validate 10_focus_en_functie section."""
        section = '10_focus_en_functie'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['opties'])

        if 'opties' in data:
            if not self._check_type(f"{section}.opties", data['opties'], list):
                return
            self._check_array_not_empty(f"{section}.opties", data['opties'])

            for i, optie in enumerate(data['opties']):
                path = f"{section}.opties[{i}]"
                if not isinstance(optie, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(optie).__name__}"))
                    continue

                # Check optie has titel or korte_titel
                if 'korte_titel' not in optie and 'titel' not in optie:
                    self.errors.append(ValidationError(path, "Optie should have 'korte_titel' or 'titel'", "warning"))

    def _validate_kalender(self):
        """Validate 11_kalender section."""
        section = '11_kalender'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['dagen'])

        if 'dagen' in data:
            if not self._check_type(f"{section}.dagen", data['dagen'], list):
                return
            self._check_array_not_empty(f"{section}.dagen", data['dagen'])

            for i, dag in enumerate(data['dagen']):
                path = f"{section}.dagen[{i}]"
                if not isinstance(dag, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(dag).__name__}"))
                    continue

                if 'datum' not in dag:
                    self.errors.append(ValidationError(f"{path}.datum", "Missing datum"))

    def _validate_hoorders(self):
        """Validate 12_representatieve_hoorders section."""
        section = '12_representatieve_hoorders'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['personas'])

        if 'personas' in data:
            if not self._check_type(f"{section}.personas", data['personas'], list):
                return
            self._check_array_not_empty(f"{section}.personas", data['personas'])

            for i, persona in enumerate(data['personas']):
                path = f"{section}.personas[{i}]"
                if not isinstance(persona, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(persona).__name__}"))
                    continue

                # Check persona has naam
                if 'naam' not in persona:
                    self.errors.append(ValidationError(f"{path}.naam", "Missing naam", "warning"))

    def _validate_gebeden(self):
        """Validate 14_gebeden section."""
        section = '14_gebeden'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['gebeden'])

        if 'gebeden' in data:
            if not self._check_type(f"{section}.gebeden", data['gebeden'], dict):
                return

            gebeden = data['gebeden']
            expected_gebeden = ['drempelgebed', 'kyrie', 'epiclese', 'dankgebed', 'voorbeden']

            for gebed in expected_gebeden:
                if gebed not in gebeden:
                    self.errors.append(ValidationError(f"{section}.gebeden.{gebed}", f"Missing {gebed}", "warning"))
                elif gebeden[gebed] is not None and isinstance(gebeden[gebed], dict):
                    gebed_data = gebeden[gebed]
                    # Check gebed has tekst, gebedstekst, or cirkels (for voorbeden)
                    has_content = (
                        'tekst' in gebed_data or
                        'gebedstekst' in gebed_data or
                        'cirkels' in gebed_data  # voorbeden uses cirkels structure
                    )
                    if not has_content:
                        self.errors.append(ValidationError(
                            f"{section}.gebeden.{gebed}",
                            "Gebed should have 'tekst', 'gebedstekst', or 'cirkels'",
                            "warning"
                        ))

    def _validate_kindermoment(self):
        """Validate 15_kindermoment section."""
        section = '15_kindermoment'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['kindermoment_opties'])

        if 'kindermoment_opties' in data:
            if not self._check_type(f"{section}.kindermoment_opties", data['kindermoment_opties'], list):
                return
            self._check_array_not_empty(f"{section}.kindermoment_opties", data['kindermoment_opties'])

            for i, optie in enumerate(data['kindermoment_opties']):
                path = f"{section}.kindermoment_opties[{i}]"
                if not isinstance(optie, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(optie).__name__}"))
                    continue

                if 'titel' not in optie:
                    self.errors.append(ValidationError(f"{path}.titel", "Missing titel", "warning"))

    def _validate_bijbelteksten(self):
        """Validate Bijbelteksten section."""
        section = 'Bijbelteksten'
        if section not in self.data or not isinstance(self.data[section], dict):
            return

        data = self.data[section]
        self._check_required_keys(section, data, ['grondtekst', 'nbv21', 'naardense_bijbel'])

        for vertaling in ['grondtekst', 'nbv21', 'naardense_bijbel']:
            if vertaling not in data:
                continue

            if not self._check_type(f"{section}.{vertaling}", data[vertaling], list):
                continue

            for i, perikoop in enumerate(data[vertaling]):
                path = f"{section}.{vertaling}[{i}]"
                if not isinstance(perikoop, dict):
                    self.errors.append(ValidationError(path, f"Expected object, got {type(perikoop).__name__}"))
                    continue

                # Check required perikoop fields
                if vertaling == 'grondtekst':
                    if 'book_original' not in perikoop:
                        self.errors.append(ValidationError(f"{path}.book_original", "Missing book_original"))
                else:
                    if 'book' not in perikoop:
                        self.errors.append(ValidationError(f"{path}.book", "Missing book"))

                if 'chapter' not in perikoop:
                    self.errors.append(ValidationError(f"{path}.chapter", "Missing chapter"))

                if 'verses' not in perikoop:
                    self.errors.append(ValidationError(f"{path}.verses", "Missing verses"))
                elif isinstance(perikoop['verses'], list):
                    for j, verse in enumerate(perikoop['verses']):
                        verse_path = f"{path}.verses[{j}]"
                        if not isinstance(verse, dict):
                            self.errors.append(ValidationError(verse_path, f"Expected object, got {type(verse).__name__}"))
                        elif 'verse' not in verse:
                            self.errors.append(ValidationError(f"{verse_path}.verse", "Missing verse number"))
                        elif 'text' not in verse:
                            self.errors.append(ValidationError(f"{verse_path}.text", "Missing text"))

    def print_report(self):
        """Print validation report."""
        if not self.errors:
            print("✓ Validation passed - no errors found")
            return

        # Group by severity
        errors = [e for e in self.errors if e.severity == "error"]
        warnings = [e for e in self.errors if e.severity == "warning"]
        infos = [e for e in self.errors if e.severity == "info"]

        print(f"\nValidation Report")
        print("=" * 60)
        print(f"Errors: {len(errors)}, Warnings: {len(warnings)}, Info: {len(infos)}")
        print()

        if errors:
            print("ERRORS:")
            print("-" * 40)
            for e in errors:
                print(f"  ✗ {e.path}: {e.message}")
            print()

        if warnings:
            print("WARNINGS:")
            print("-" * 40)
            for e in warnings:
                print(f"  ⚠ {e.path}: {e.message}")
            print()

        if infos:
            print("INFO:")
            print("-" * 40)
            for e in infos:
                print(f"  ℹ {e.path}: {e.message}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py <json_file>")
        print("       python validate_json.py docs/voorbeeld_02.json")
        sys.exit(1)

    file_path = sys.argv[1]

    print(f"Validating: {file_path}")
    print("=" * 60)

    validator = LiturgischeAnalyseValidator()
    is_valid = validator.validate_file(file_path)
    validator.print_report()

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
