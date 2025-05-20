# This script fetches a Google Docs document, parses it to extract a table of
# characters, and arranges them into a grid to reveal a secret message.
# Author: Arthur Bowers
# Date: 19/05/2025

import requests
from bs4 import BeautifulSoup as bs


def fetch_and_parse_doc(url: str) -> str:
    """
    Fetches a Google Docs document and returns its HTML content.
    :param url: The URL of the Google Docs document.
    :return: None
    """
    try:
        # Fetch the document
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as err:
        print(f"Error fetching the document: {err}")
        return None


def parse_table_characters(table_str: str) -> list:
    """
    Parses the table from the document and extracts characters.
    :param table_str: The HTML content of the table.
    :return characters: A list of tuples containing (x, y, character).
    """
    soup = bs(table_str, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found in the document.")
        return []

    rows = table.find_all('tr')
    characters = []

    for row in rows[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 3:
            try:
                x = int(cells[0].get_text().strip())
                char = cells[1].get_text().strip()
                y = int(cells[2].get_text().strip())

                if char:
                    characters.append((x, y, char))
            except ValueError:
                continue
    return characters


def arrange_chars_into_grid(characters: list, x_scale=6, y_scale=13) -> list:
    """
    Arranges characters into a grid based on their x and y coordinates.
    :param characters: A list of tuples containing (x, y, character).
    :param x_scale: The scale factor for the x-axis.
    :param y_scale: The scale factor for the y-axis.
    :return: A 2D list representing the grid.
    """
    if not characters:
        return []

    max_x = max(x for x, _, _ in characters)
    max_y = max(y for _, y, _ in characters)

    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in characters:
        grid[y][x] = char

    return grid


def print_grid(grid: list) -> None:
    """
    Prints the grid in reverse order to display the secret message.
    :param grid: A 2D list representing the grid.
    :return: None
    """
    for row in reversed(grid):
        print(''.join(row))


def extract_secret_message_from_doc(url: str) -> None:
    """
    Extracts a secret message from a Google Docs document by fetching,
    parsing, and arranging characters into a grid.
    :param url: The URL of the Google Docs document.
    :return: None
    """
    html = fetch_and_parse_doc(url)
    if not html:
        return

    characters = parse_table_characters(html)
    if not characters:
        print("No characters found in the document.")
        return

    # Arrange characters into a grid
    grid = arrange_chars_into_grid(characters)
    print_grid(grid)


url = "https://docs.google.com/document/d/e/2PACX-1vSCJGXDu491Y3rRgJPVhtdsY5ivkbQ5FJMDvPyanh2F7HNk2cea9AZIHa1j-RShETAsCxKqqbZ_Vz7J/pub"
extract_secret_message_from_doc(url)
