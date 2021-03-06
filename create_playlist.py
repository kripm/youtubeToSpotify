from googleapiclient.discovery import build
import json
import youtube_dl

import requests

from secrets import spotify_token, spotify_user_id, api_key
import urllib.parse


class CreatePlaylist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # get video titles from youtube
    def get_video_titles(self):
        ydl = youtube_dl.YoutubeDL({})
        video_title_list = []

        service = build('youtube', 'v3', developerKey=api_key)
        playlist_request = service.playlistItems().list(
            part='contentDetails',
            playlistId='PL1RdbHwKcxVhivt2jwsfl1ngBrHIe0K_k'
        )

        response = playlist_request.execute()

        for video_list in response['items']:
            video_title = []
            youtube_url = 'https://www.youtube.com/watch?v='
            youtube_url += video_list['contentDetails']['videoId']

            with ydl:
                video = ydl.extract_info(youtube_url, download=False)

            video_title.append(video['artist'])
            video_title.append(video['track'])
            video_title_list.append(video_title)

        return video_title_list

    # create spotify playlist
    def create_playlist(self):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
        query = json.dumps({
            "name": "Youtube To Spotify",
            "description": "Python script to import songs in a Youtube playlist to a Spotify playlist.",
            "public": False
        })

        response = json.loads(requests.post(
            url, query, headers=header).content)
        playlist_id = response['id']

        return playlist_id

    # get spotify uri for song
    def search_songs(self, artist_name, song_name):
        song_name = urllib.parse.quote(song_name)
        url = "https://api.spotify.com/v1/search?q=artist:{}+track:{}&type=artist,track&limit=5&offset=0".format(
            artist_name, song_name)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }

        response = json.loads(requests.get(url, headers=header).content)

        try:
            song_uri = response['tracks']['items'][0]['uri']
        except:
            song_uri = ''

        return song_uri

    # add songs to new spotify playlist
    def add_songs(self):
        playlist_id = self.create_playlist()
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
        video_title_list = self.get_video_titles()

        for video_title in video_title_list:
            song_uri = self.search_songs(video_title[0], video_title[1])
            url = 'https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(
                playlist_id, song_uri)
            requests.post(url, headers=header)


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_songs()
