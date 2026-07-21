"""Command-line interface for the current Local AI Guild stage."""

import argparse
from collections.abc import Sequence

PROJECT_NAME = "Local AI Guild"
IMPLEMENTATION_STAGE = "R1: typed tool contracts and deterministic mock router"


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(prog="local-ai-guild", description=PROJECT_NAME)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("status", help="Print project identity and implementation stage")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)
    if args.command == "status":
        print(f"Project: {PROJECT_NAME}")
        print(f"Stage: {IMPLEMENTATION_STAGE}")
        return 0
    return 2
