import requests
from bs4 import BeautifulSoup
import re

class SongSection:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line_type, content):
        self.lines.append(({"type": line_type, "content": content}))

def fetch_artists(url):
    # Fetch the content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Select all <a> tags within the specified div class
        artist_links = soup.select('div.bg-componentbodycolor a[href]')
        artist_data = []
        for link in artist_links[:10]:  # Limit to first 10 artists only
            artist_name = link.text.strip()
            artist_url = link['href']
            artist_data.append((artist_name, artist_url))
        return artist_data
    else:
        print(f"Failed to retrieve the web page. Status code: {response.status_code}")
        return None

def fetch_songs_from_artist_page(artist_url):
   # Fetch the content from the artist's page URL
    response = requests.get(artist_url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Select all <a> tags within the table rows
        song_links = soup.select('table.min-w-full a[href]')
        song_data = []
        for link in song_links:
            song_title = link.text.strip()
            song_url = link['href']
            song_data.append((song_title, song_url))
        return song_data
    else:
        print(f"Failed to retrieve the artist page. Status code: {response.status_code}")
        return []

def fetch_song_content(song_url):
    # Fetch the HTML content
    response = requests.get(song_url)
    if response.status_code != 200:
        print(f"Failed to load page with status code: {response.status_code}, URL: {song_url}")
        return {}
        #raise Exception("Failed to load page")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    song_structure = []
    # Extract song sections (Chorus, Verses, etc.)
    song_tag = soup.find('pre', attrs={'transpose-ref': True})
    input_text = song_tag.get_text() if song_tag else ''
    sections = []
    current_section = None

    # Define a regex pattern for section headers
    section_pattern = re.compile(r'\[(.*?)\]')
    # Define a regex pattern for chord lines
    chord_pattern = re.compile(r'([A-G][#b]?m?(maj|min|dim|aug|sus\d*)?\d*)')

    lines = input_text.split('\n')
    for line in lines:
        # Check if the line is a section header
        section_match = section_pattern.search(line)
        if section_match:
            # Start a new section
            section_name = section_match.group(1)
            current_section = SongSection(section_name)
            sections.append(current_section)
        elif current_section:
            # Determine if the line is a chord line or a lyric line
            if chord_pattern.search(line):
                current_section.add_line('chord', line)
            else:
                current_section.add_line('lyric', line)

    return sections

def start(url):
    artists = fetch_artists(url)
    artists = artists[:3]

    for artist_name, artist_url in artists:
        print(f"Fetching songs for artist: {artist_name}")
        songs = fetch_songs_from_artist_page(artist_url)
        for song_title, song_url in songs:
            song_content = fetch_song_content(song_url)
            print(f"Artist: {artist_name}, Song: {song_title}, Song URL: {song_url}")
            for content in song_content:
                print(f"  {content.name}")
                for line in content.lines:
                    print(f"  {line['type']}: {line['content']}")



