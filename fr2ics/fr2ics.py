# -*- coding: utf-8 -*-

"""Main module."""

import os
from datetime import timedelta, datetime

import ics
import arrow
import pendulum

_csv = []
_csv_path = ""
_teams = None

def _get_csv(path):
    """Read in CSV from path"""
    global _csv
    if len(_csv) == 0 or _csv_path != path:
        with open(path, 'r') as fh:
            for line in fh.readlines():
                _csv.append(line.split(','))
    return _csv

def get_skip_calendars(path, rounds=5, skip=None):
    teams = get_teams(path)
    if skip:
        for teamid, v in teams.items():
            if v['name'].lower() == skip.lower():
                cals = {teamid: ics.Calendar()}
    else:
        cals = {teamid: ics.Calendar() for teamid in teams.keys()}

    for event in _get_events(path):
        for teamid, cal in cals.items():
            if teams[teamid]['name'] in event.name:
                cal.events.add(event)
    
    for teamid, cal in cals.items():
        output_path = f"{teams[teamid]['name']}.ics"
        _write_calendar(cal, output_path)


def get_calendar(path, output_path=None, rounds=5):
    cal = ics.Calendar()
    output_path = os.path.splitext(path)[0] + '.ics'

    for event in _get_events(path):
        cal.events.add(event)

    _write_calendar(cal, output_path)

def _write_calendar(cal, output_path):
    with open(output_path, 'w') as fh:
        fh.writelines(cal)

def _get_events(path, rounds=5, location='750 Daly St S, Winnipeg, MB R3L 2N2',
                organizer_email='frccmixed@gmail.com', organizer_name='Cam Barth'):
    contacts = get_teams(path)

    for game in get_games(path, rounds):
        skips = [contacts[game['teams'][idx]] for idx in [0,1]]
        # print(game)
        yield ics.Event(
            name=f"{skips[0]['name']} vs {skips[1]['name']} on Sheet {game['sheet']}",
            begin=_get_datetime(game['day'], game['month'], game['time']),
            duration={"hours": 2},
            location=location,
            alarms=[ics.alarm.DisplayAlarm(trigger=timedelta(minutes=90))],
            categories=['FRCC Friday Night Mixed', 'Curling', 'Sports'],
            organizer=ics.Organizer(email=organizer_email, common_name=organizer_name),
            attendees=[ics.Attendee(email=skip['email'], common_name=skip['name']) for skip in skips],
            description=f"Contact Details: {skips[0]['name']} ({skips[0]['email']}) Ph: {skips[0]['phone']} /// {skips[1]['name']} ({skips[1]['email']}) Ph: {skips[1]['phone']}"
        )


def _get_datetime(day, month, time, tz="America/Winnipeg"):
    now = datetime.now()
    day = str(day).zfill(2) # front-pad day with a zero
    month = str(arrow.get(month, "MMM").month).zfill(2) # parse month word, pad with a zero
    year = now.year if now.month <= int(month) else now.year + 1
    time = "19:10" if time.startswith('7') else "21:20"
    # eg: 2013-05-11T21:23+07:00
    return pendulum.parse(f"{year}-{month}-{day}T{time}", tz=tz).isoformat()


def get_games(path, rounds=5):
    csv = _get_csv(path)

    # sched rows start at row 8
    # month and day were merged so contents in every 2nd row
    month_pos = lambda rnd: (6 + (2*rnd), 1)
    day_pos = lambda rnd: (6 + (2*rnd), 2)

    for rnd in range(0,rounds):
        for time in ['7:10pm', '9:20pm']:
            sheet = 0
            start_row = 6 if time == '7:10pm' else 7
            for teams in _process_gameteams(rnd, start_row):
                sheet += 1
                yield {
                    'day': csv[day_pos(rnd)[0]][day_pos(rnd)[1]],
                    'month': csv[month_pos(rnd)[0]][month_pos(rnd)[1]],
                    'time': time,
                    'teams': teams,
                    'sheet': sheet
                }

def _process_gameteams(rnd, start_row):
    game_pos = lambda rnd: [(start_row + (2*rnd), col) for col in range(4,10)]
    for pos in game_pos(rnd):
        yield [team.strip(' ') for team in _csv[pos[0]][pos[1]].split('-')]

def get_teams(path):
    global _teams
    if not _teams:
        csv = _get_csv(path)

        # only extracting the D teams
        team_rows = range(18,30)
        team_cols = [(1,2), (6,7)]

        # have to read all contact infos tho
        con_rows = range(1,26)
        conname_col = 14
        connum_col = 15
        conemail_col = 16

        # read contact info section
        cons = { 
            _cleanname(csv[row][conname_col]): {
                'phone': csv[row][connum_col],
                'email': csv[row][conemail_col].strip("\n"),
            } for row in con_rows
        }
        # print(cons)

        # read teams and merge in contact info
        _teams = {
            csv[row][cols[0]]: {
                'name': csv[row][cols[1]],
                'phone': cons[csv[row][cols[1]]]['phone'],
                'email': cons[csv[row][cols[1]]]['email'],
            } for row in team_rows for cols in team_cols
        }
    # print(teams)
    return _teams

def _cleanname(name):
    # we can assume case matches
    # need to remove first names/initials tho
    words = name.split(' ')
    return words[len(words)-1]