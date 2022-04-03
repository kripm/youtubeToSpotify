import json

import requests

from secrets import spotify_token, spotify_user_id

class CreatePlaylist:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # log into youtube
    def get_youtube_client():
        pass

    #get video titles from youtube playlist
    def get_video_titles():
        pass

    # create spotify playlist
    def create_playlist(self):
        url = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
        query = json.dumps({
            "name": "Youtube To Spotify",
            "description": "Python script to import songs in a Youtube playlist to a Spotify playlist.",
            "public": False
        })

        response = requests.post(url, query, headers=header)
        print(response)

    # get spotify uri for song
    def search_songs():
        pass

    # add songs to new spotify playlist
    def add_songs():
        pass


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.create_playlist()
