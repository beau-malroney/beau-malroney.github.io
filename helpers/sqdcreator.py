from argparse import ArgumentParser
from datetime import date, timedelta
from pathlib import Path


def create_file(target_dir: Path, target_date: date) -> Path:
    filename = f"{target_date.strftime('%Y-%m-%d')}-side-quest-dispatch.md"
    filepath = target_dir / filename
    filepath.write_text("# Side Quest\n", encoding="utf-8")
    return filepath


def date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


parser = ArgumentParser()
parser.add_argument(
    "-p",
    "--path",
    default=".",
    help="Directory where files should be created"
)
parser.add_argument(
    "--start",
    type=date.fromisoformat,
    help="Start date in YYYY-MM-DD format"
)
parser.add_argument(
    "--end",
    type=date.fromisoformat,
    help="End date in YYYY-MM-DD format"
)

args = parser.parse_args()

target_dir = Path(args.path)
target_dir.mkdir(parents=True, exist_ok=True)

if args.start or args.end:
    if not (args.start and args.end):
        parser.error("You must provide both --start and --end together.")
    if args.start > args.end:
        parser.error("--start must be earlier than or equal to --end.")

    for d in date_range(args.start, args.end):
        created = create_file(target_dir, d)
        print(f"Created: {created}")
else:
    created = create_file(target_dir, date.today())
    print(f"Created: {created}")