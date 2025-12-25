#!/usr/bin/env python3
"""
Count tokens in all markdown files per church.

Usage:
    python count_tokens.py [--output-dir PATH]
"""

import argparse
from pathlib import Path

# Try to use tiktoken for accurate counting, fall back to estimation
try:
    import tiktoken
    ENCODER = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(ENCODER.encode(text))

    TOKENIZER = "tiktoken (cl100k_base)"
except ImportError:
    def count_tokens(text: str) -> int:
        # Rough estimation: ~4 characters per token for most text
        return len(text) // 4

    TOKENIZER = "estimation (chars/4)"


def count_tokens_for_church(church_dir: Path) -> dict:
    """Count tokens in all markdown files for a church directory."""
    results = {
        "church": church_dir.name,
        "files": {},
        "total": 0
    }

    # Find all markdown files recursively
    for md_file in sorted(church_dir.rglob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            tokens = count_tokens(content)
            relative_path = md_file.relative_to(church_dir)
            results["files"][str(relative_path)] = tokens
            results["total"] += tokens
        except Exception as e:
            print(f"  Warning: Could not read {md_file}: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Count tokens in markdown files per church")
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path(__file__).parent / "output",
        help="Path to output directory containing church folders (default: ./output)"
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Path to a single file to count tokens for"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show per-file token counts"
    )
    args = parser.parse_args()

    # Handle single file mode
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        
        try:
            content = args.file.read_text(encoding="utf-8")
            tokens = count_tokens(content)
            print(f"File: {args.file.name}")
            print(f"Tokens: {tokens:,}")
            return 0
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1

    output_dir = args.output_dir

    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        return 1

    print(f"Tokenizer: {TOKENIZER}")
    print(f"Scanning: {output_dir}\n")

    # Find all church directories (directories containing .md files)
    church_dirs = sorted([
        d for d in output_dir.iterdir()
        if d.is_dir() and list(d.glob("*.md"))
    ])

    if not church_dirs:
        print("No church directories with markdown files found.")
        return 1

    all_results = []
    grand_total = 0

    for church_dir in church_dirs:
        result = count_tokens_for_church(church_dir)
        all_results.append(result)
        grand_total += result["total"]

        print(f"{result['church']}")

        if args.verbose:
            for filename, tokens in result["files"].items():
                print(f"  {filename}: {tokens:,}")

        print(f"  Total: {result['total']:,} tokens\n")

    # Summary
    print("-" * 50)
    print(f"{'SUMMARY':^50}")
    print("-" * 50)

    # Sort by token count descending
    sorted_results = sorted(all_results, key=lambda x: x["total"], reverse=True)

    for result in sorted_results:
        pct = (result["total"] / grand_total * 100) if grand_total > 0 else 0
        print(f"{result['church'][:40]:<40} {result['total']:>8,} ({pct:4.1f}%)")

    print("-" * 50)
    print(f"{'GRAND TOTAL':<40} {grand_total:>8,}")
    print(f"{'Churches':<40} {len(all_results):>8}")
    print(f"{'Avg per church':<40} {grand_total // len(all_results) if all_results else 0:>8,}")

    return 0


if __name__ == "__main__":
    exit(main())
