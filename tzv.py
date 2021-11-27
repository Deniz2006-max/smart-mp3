# import spotipy
# import tkinter
#
# from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
# client_id = "e69759b4d1e14ae4ae5f67ffb486773e"
# client_secret = "8e503bea3ac7469496cfd93485ee7786"
# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
#                                                                               client_secret=client_secret))
# # eminem = spotify.artist("7dGJo4pcD2V6oG8kP0tJRR")
# # print(eminem)
# #
# # man = spotify.recommendations(seed_artists="7dGJo4pcD2V6oG8kP0tJRR")
#
# man = spotify.new_releases(country="TR")
# print(man)
# # for i in range(len(man["tracks"])):
# #
# #     man = man["tracks"][i]["name"]
# #     print(man)
#
# def kazanc(x):
#     p = 0
#     c = 0
#     e = 0
#     for i in (x.keys()):
#         if i == "maliyet":
#             p += x[i]
#         if i == "satış":
#             c += x[i]
#         if i == "envanter":
#             e += x[i]
#     toplam_maliyet = e * p
#     toplam_gelir =  e * c
#     toplam_kazanc = toplam_gelir - toplam_maliyet
#     return toplam_kazanc
#
#
# print(kazanc({"maliyet":32.67,
#               "satış": 45.00,
#               "envanter": 1200}))



def format_check(x):
    numbers = ["0","1","2","3","4","5","6","7","8","9"]
    if len(x) == 14:
        p = 0
        for char in x :
            if char in numbers:
                p += 1
                print(char)

        if p == 10:
            if x[0] == "(" and x[4] == ")" and x[9] == "-":
                return True
        else:
            return False
    else:
        return False


print(format_check("(223) 456-7890"))







