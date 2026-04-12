"""
JSON → Database Loader
======================
Loads qualification data from a Univice-format JSON file (produced by
uj_reader.py or any other institution reader) into the Django database.

Usage as standalone script:
    python manage.py load_qualifications path/to/uj_all_pages.json

Usage as a library:
    from qualifications.readers.json_loader import load_from_json
    stats = load_from_json("path/to/file.json")
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from qualifications.models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)


def load_from_json(
    source: Union[str, Path, dict],
    dry_run: bool = False,
    log_fn=None,
) -> Dict[str, Any]:
    """
    Load qualifications from a JSON file or dict into the database.

    Args:
        source: Path to a JSON file, or an already-parsed dict.
        dry_run: If True, validate but don't write to the database.
        log_fn: Optional callable(message: str) for progress output.

    Returns:
        Stats dict with counts of created/updated/skipped records.
    """
    if log_fn is None:
        log_fn = lambda msg: None  # noqa: E731

    # Load data
    if isinstance(source, dict):
        data = source
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"JSON file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    stats = {
        "institution_created": False,
        "qualifications_created": 0,
        "qualifications_updated": 0,
        "qualifications_skipped": 0,
        "aps_rules_created": 0,
        "subject_requirements_created": 0,
        "selection_requirements_created": 0,
        "errors": [],
    }

    institution_name = data.get("name", "")
    institution_abbr = data.get("abbr", "")
    qualifications = data.get("qualifications", [])

    if not institution_name:
        raise ValueError("JSON must have a top-level 'name' field for the institution")

    log_fn(f"Loading {len(qualifications)} qualifications for {institution_name}")

    if dry_run:
        log_fn("DRY RUN — no database writes")
        for q in qualifications:
            _validate_qualification(q, stats)
        return stats

    # Create or update institution
    institution, created = Institution.objects.update_or_create(
        name=institution_name,
        defaults={"abbreviation": institution_abbr},
    )
    stats["institution_created"] = created
    log_fn(f"{'Created' if created else 'Updated'} institution: {institution}")

    for q_data in qualifications:
        try:
            _load_qualification(institution, q_data, stats, log_fn)
        except Exception as e:
            stats["errors"].append(f"{q_data.get('name', '?')}: {e}")
            log_fn(f"  ERROR: {e}")

    log_fn(
        f"Done: {stats['qualifications_created']} created, "
        f"{stats['qualifications_updated']} updated, "
        f"{stats['qualifications_skipped']} skipped, "
        f"{len(stats['errors'])} errors"
    )
    return stats


def _validate_qualification(q: dict, stats: dict) -> None:
    """Validate a qualification dict without writing to DB."""
    slug = q.get("id", "")
    name = q.get("name", "")
    minimum_aps = q.get("minimum_aps")

    if not slug or not name:
        stats["qualifications_skipped"] += 1
        return
    if minimum_aps is None:
        stats["qualifications_skipped"] += 1
        return
    stats["qualifications_created"] += 1


def _load_qualification(
    institution: Institution,
    q_data: dict,
    stats: dict,
    log_fn,
) -> None:
    """Load a single qualification and its related objects."""
    slug = q_data.get("id", "")
    name = q_data.get("name", "")
    minimum_aps = q_data.get("minimum_aps")

    if not slug or not name:
        stats["qualifications_skipped"] += 1
        log_fn(f"  Skipped (missing slug/name): {q_data}")
        return

    if minimum_aps is None:
        stats["qualifications_skipped"] += 1
        log_fn(f"  Skipped (no APS): {name}")
        return

    qual, created = Qualification.objects.update_or_create(
        slug=slug,
        defaults={
            "institution": institution,
            "name": name,
            "qualification_code": q_data.get("qualification_code", ""),
            "faculty": q_data.get("faculty") or "",
            "description": q_data.get("description", ""),
            "minimum_aps": minimum_aps,
            "qualification_type": q_data.get("qualification_type") or "",
            "duration": q_data.get("duration") or "",
            "campus": q_data.get("campus") or "",
        },
    )

    if created:
        stats["qualifications_created"] += 1
    else:
        stats["qualifications_updated"] += 1

    action = "Created" if created else "Updated"
    log_fn(f"  {action}: {name} ({slug})")

    # Clear and re-create related objects
    qual.aps_rules.all().delete()
    qual.subject_requirements.all().delete()
    qual.selection_requirements.all().delete()

    # APS rules
    for rule_data in q_data.get("aps_rules", []):
        rule = APSRule.objects.create(
            qualification=qual,
            rule_type=rule_data.get("type", "subject_dependent_minimum_aps"),
        )
        stats["aps_rules_created"] += 1
        for cond in rule_data.get("conditions", []):
            APSRuleCondition.objects.create(
                rule=rule,
                subject=cond.get("subject", ""),
                minimum_level=cond.get("minimum_level") or 0,
                min_aps=cond.get("min_aps") or 0,
            )

    # Subject requirements
    for req_type in ("mandatory", "one_of", "disallowed"):
        for req in q_data.get("subject_requirements", {}).get(req_type, []):
            SubjectRequirement.objects.create(
                qualification=qual,
                requirement_type=req_type,
                subject=req.get("subject", ""),
                minimum_level=req.get("minimum_level") or 0,
            )
            stats["subject_requirements_created"] += 1

    # Selection requirements
    for sel in q_data.get("selection_requirements", []):
        SelectionRequirement.objects.create(
            qualification=qual,
            selection_type=sel.get("type", "other"),
            required=sel.get("required", False),
            notes=sel.get("notes"),
        )
        stats["selection_requirements_created"] += 1
