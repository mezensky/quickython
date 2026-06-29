"""Command-line entry point for quickython.

Run with ``python -m quickython`` or the installed ``quickython`` script.
Uses the stdlib ``argparse`` to stay dependency-free; swap in Typer or Click
here if you want a richer CLI.
"""

import argparse
from collections.abc import Sequence

from quickython.example import greet


def build_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="quickython",
        description="Print a greeting (sample CLI).",
    )
    parser.add_argument("name", nargs="?", default="World", help="Who to greet.")
    parser.add_argument(
        "-s",
        "--salutation",
        default="Hello",
        help="Greeting word to use (default: %(default)s).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI.

    Args:
        argv: Argument list (defaults to ``sys.argv[1:]`` when ``None``).

    Returns:
        Process exit code (``0`` on success).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        print(greet(args.name, salutation=args.salutation))
    except ValueError as exc:
        parser.error(str(exc))  # raises SystemExit(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
