'''
Copyright (C) 2024  __retr0.init__

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''
import requests
from bs4 import BeautifulSoup
import re

def get_youtube_channel_name(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        channel_name = soup.find('meta', itemprop='name')['content']
        return channel_name
    except Exception as e:
        print(f"An error occurred: ")
        return e


def is_youtube_url(url):
    pattern = r'^https://www\.youtube\.com/@\w+$'
    if re.match(pattern, url):
        return True
    else:
        return False

'''
url = 'https://www.youtube.com/@Faide'
name = get_youtube_channel_name(url)

if name:
    print(f'YouTube channel name: {name}')
else:
    print('Could not extract YouTube channel name.')'''
'''channel = 'https://www.youtube.com/@Faide'

                    #getting html of the /videos page
html = requests.get(channel+"/videos").text

                  
try:
    latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    print(f'{latest_video_url}')
except Exception as e:

    print(f'A error occured:{e}')'''
