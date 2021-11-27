import spotipy
from spotipy.oauth2 import SpotifyClientCredentials




import spacy
client_id = "e69759b4d1e14ae4ae5f67ffb486773e"
client_secret = "8e503bea3ac7469496cfd93485ee7786"


username = "YOUR USERNAME"

#note that I extended the scope to also modify non-public playlists
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

redirect_uri = "THE REDIRECT URI FOR YOUR APP"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
#
# token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
# if token:
#     sp = spotipy.Spotify(auth=token)
# else:
#     print("Can't get token for", username)

seed_tracks = playlist_df["track_id"].tolist()

#create recommendation df from multiple recommendations
recomm_dfs = []
for i in range(5,len(seed_tracks)+1,5):
    recomms = sp.recommendations(seed_tracks = seed_tracks[i-5:i],limit = 25)
    recomms_df = append_audio_features(create_df_recommendations(recomms),sp)
    recomm_dfs.append(recomms_df)
recomms_df = pd.concat(recomm_dfs)
recomms_df.reset_index(drop = True, inplace = True)