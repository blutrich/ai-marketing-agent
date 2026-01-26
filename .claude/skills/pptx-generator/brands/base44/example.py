#!/usr/bin/env python3
"""
Example: Generate Base44-branded presentation using the generate module.
Run: python3 example.py
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from generate import (
    create_presentation,
    add_title_slide,
    add_stats_slide,
    add_two_column_slide,
    add_quote_slide,
    add_cta_slide,
    add_content_slide,
    add_cards_slide,
    save_presentation,
)


def main():
    # Create presentation
    prs = create_presentation()

    # Slide 1: Title
    add_title_slide(
        prs,
        headline="Safe Testing Just Dropped",
        subtitle="Test forms and automations without breaking production"
    )

    # Slide 2: Feature cards
    add_cards_slide(
        prs,
        title="Test Without Fear",
        cards=[
            ("Test Data Toggle", "Simulate submissions and create test records with one click"),
            ("Safe Database", "Your real data and automations stay completely protected"),
            ("Scale Better", "Experiment freely and release with confidence"),
        ]
    )

    # Slide 3: CTA
    add_cta_slide(
        prs,
        headline="Start Building Today",
        button_text="base44.com"
    )

    # Save
    output_path = save_presentation(prs, "example-output")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
