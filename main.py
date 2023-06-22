from youtube import Youtube
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os

scope = 'playlist-modify-public'

def main():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.environ["SPOTIPY_CLIENT_ID"], client_secret=os.environ["SPOTIPY_CLIENT_SECRET"], redirect_uri=os.environ["SPOTIPY_REDIRECT_URI"], open_browser=True))
    yt = Youtube()
    user_id = sp.me()['id']
    
    yt_playlist_id = input("Enter youtube playlist id: ")
    spotify_playlist_name = input("Enter a name for your spotify playlist: ")
    spotify_playlist_id = sp.user_playlist_create(user_id, spotify_playlist_name)['id']
    print(spotify_playlist_id)
    songs = yt.get_songs_from_playlist(yt_playlist_id)

    for song in songs:
        song_result = sp.search('{} {}'.format(song.artist, song.title), limit=1, type='track')
        
        if not song_result or len(song_result) == 0 or not song_result['tracks']['items'][0]:
            print(f"{song.artist} - {song.title} was not found!")
            continue

        song_uri = song_result['tracks']['items'][0]['uri']

        if not song_uri:
            print(f"{song.artist} - {song.title} was not found!")
            continue
        
        was_added = sp.playlist_add_items(spotify_playlist_id, [song_uri])

        if was_added:
            print(f'{song.artist} - {song.title} was added to playlist.')
        
    total_songs_added = sp._num_playlist_songs(spotify_playlist_id)
    print(f'Added {total_songs_added} songs out of {len(songs)}')

if __name__ == "__main__":
    main()
