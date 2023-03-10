#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from datetime import datetime
import argparse
from sys import exit
from rich import print
from ctfl import __version__


def main():
    url = 'https://ctftime.org/event/list/upcoming'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5\
        37.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    parser = parseArgs()
    args = parser.parse_args()

    months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}

    if (args.next):
        month = months[int(datetime.now().strftime("%m")) + 1]
    elif (args.all):
        month = None
    elif (args.version):
        print("[bold]ctfl {}[/]".format(__version__))
        exit(0)
    else:
        month = datetime.now().strftime("%b")
    try:
        data = extract_data(url, headers, month)
        print_data(data)
    except KeyboardInterrupt:
        exit(1)
    except Exception:
        print("[[bold red]-[/]] Unexpected error occurred, Try again...")


def parseArgs():
    parser = argparse.ArgumentParser(description="CTFTime Upcoming CTF Events Lists")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
            "-n",
            "--next",
            action="store_true",
            help="Get the list of events for the next month"
    )
    group.add_argument(
            "-a",
            "--all",
            action="store_true",
            help="List all available CTFs on the event list"
    )
    group.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Prints the version of the tool"
    )
    return parser


def extract_data(url, headers, month):
    req = requests.get(url, headers=headers)

    soup = BeautifulSoup(req.text, 'html.parser')
    events_table = soup.find_all('table')[0]

    names = []
    dates = []
    styles = []
    locations = []
    weights = []
    links = []
    base_link = "https://ctftime.org"

    if (month is not None):
        for i in events_table.find_all('tr')[1::]:
            columns = i.find_all('td')
            date = columns[1].text.strip()
            if (month in date):
                dates.append(date)
                names.append(columns[0].a.text.strip())
                links.append(base_link + columns[0].a.get('href').strip())
                styles.append(columns[2].text.strip())
                locations.append(columns[3].text.strip())
                weights.append(columns[4].text.strip())
            else:
                pass
    else:
        for i in events_table.find_all('tr')[1:]:
            columns = i.find_all('td')
            names.append(columns[0].a.text.strip())
            links.append(base_link + columns[0].a.get('href').strip())
            dates.append(columns[1].text.strip())
            styles.append(columns[2].text.strip())
            locations.append(columns[3].text.strip())
            weights.append(columns[4].text.strip())

    data = [names, dates, styles, locations, weights, links]
    return data


def print_data(data):
    table = Table(title="CTFTime CTF Events")

    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Date", justify="center", style="cyan")
    table.add_column("Style", justify="center", style="cyan")
    table.add_column("Location", justify="center", style="cyan")
    table.add_column("Weight", justify="right", style="cyan")

    for i in range(len(data[0])):
        table.add_row(data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], style="link " + data[5][i])

    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()
