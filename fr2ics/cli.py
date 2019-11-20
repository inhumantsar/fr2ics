# -*- coding: utf-8 -*-

"""Console script for fr2ics."""
import sys
import click

import fr2ics.fr2ics as fr2ics


@click.command()
@click.option("-f", "path", default='frcc.csv', help="Path to CSV")
@click.option("--rounds", default=5, type=click.INT, help="Number of rounds in spreadsheet")
@click.option("--skips", is_flag=True, help="Generate calendars for skips")
@click.option("--only-skip", default=None, type=click.STRING, help="Only generate cal for specified skip")
def main(path, rounds, skips, only_skip):
    """Console script for fr2ics."""
    if not skips:
        fr2ics.get_calendar(path, rounds=rounds)
    else:
        fr2ics.get_skip_calendars(path, rounds, only_skip)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
