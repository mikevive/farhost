"""Entry point for devflow: handles --status flag or launches TUI."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="DevFlow - Time tracking TUI")
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print active timer status and exit",
    )
    args = parser.parse_args()

    if args.status:
        from devflow.cli import print_status
        from devflow.db.connection import get_connection

        conn = get_connection()
        try:
            output = print_status(conn)
            print(output)
        finally:
            conn.close()
        sys.exit(0)

    from devflow.app import DevFlowApp

    app = DevFlowApp()
    app.run()


if __name__ == "__main__":
    main()
