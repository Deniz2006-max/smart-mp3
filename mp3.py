import pygame
import tkinter
import wikipedia
from tkinter import filedialog
from PIL import ImageTk, Image
import stagger
import io
from tkinter import messagebox
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import tkinter.font as font
import json
import os
import requests
import spacy

from ttkthemes import ThemedStyle
import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials





client_id = "e69759b4d1e14ae4ae5f67ffb486773e"
client_secret = "8e503bea3ac7469496cfd93485ee7786"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
                                                                              client_secret=client_secret))
root = tkinter.Tk()
my_frame = tkinter.Frame()
my_frame.pack()
my_listbox = tkinter.Listbox(my_frame, background="grey" ,width=100, height=20)
my_listbox.pack(side="top")




def replacing(x):
    """
    It is created to extract the name of the song and name of the singer.
    :param x: It is the object which the function will extract the specified info.
    :return: It returns the extracted part.
    """

    if x:
        x = str(x)
        x = x.replace("C:/Users/user/Downloads", "")
        x = x.replace("('/", "")
        x = x.replace("',)", "")
        x = x.replace(".mp3", "")
        x = x.replace("/", "")
        return x


storing_list = list()

song = None
def add_song():
    global song
    """
    it is a function which adds the song you have selected from your downloads to listbox.
    However, it can only add one song.
    """
    song = filedialog.askopenfilename(initialdir="C:/Users/user/Downloads", filetypes=("mp3 files", "* mp3"))
    print(type(song))
    storing_list.append(song)
    song = replacing(song)
    my_listbox.insert("end", song)


def add_many_song():
    global song
    """
    it has a similar function as the previous one, this time the only difference is
    you can add more than one song to your listbox.
    :return:
    """
    songs = filedialog.askopenfilenames(initialdir="C:/Users/user/Downloads", filetypes=("mp3 files", "* mp3"))

    for song in songs:
        storing_list.append(song)
        song = replacing(song)
        my_listbox.insert("end", song)



pygame.mixer.init()

# def delete():
#     global playing
#     """
#     A function to delete a song.It also stops the currently playing songs.
#     :return: Nothing
#     """
#     try:
#         pygame.mixer.music.stop()
#         my_listbox.selection_clear("active")
#         playing += 1
#         global stopped
#         stopped = True
#         # similar = False
#
#         my_listbox.delete("anchor")
#         pygame.mixer.music.stop()
#
#     except NameError:
#         pass

def save():
    """This function saves all the songs into a table called songs.It enables you tor retrieve songs.However, It doesn't
    save the song if it is already saved."""
    conn = sqlite3.connect("song.db")
    conn.execute("CREATE TABLE IF NOT EXISTS songs (song TEXT, number NUMBER)")
    c = conn.cursor()
    for songs in storing_list:

        c.execute("INSERT  INTO songs SELECT :song_name WHERE NOT EXISTS(SELECT 1 FROM songs WHERE song = :song_name) ",
                  {"song_name" : songs}, )

    conn.commit()
    conn.close()

#
# def query():
#     """This function is created in case you want to query the content of the songs table"""
#     conn = sqlite3.connect("song.db")
#     conn.execute("CREATE TABLE IF NOT EXISTS songs (song TEXT)")
#
#     c = conn.cursor()
#     c.execute("SELECT * ,oid FROM songs")
#     print(c.fetchall())
#
#     conn.commit()
#     conn.close()


def retrieve_songs():
    """Thıs function will retrieve the songs which were saved previously."""
    conn = sqlite3.connect("song.db")
    conn.execute("CREATE TABLE IF NOT EXISTS songs (song TEXT)")

    c = conn.cursor()

    for saved_song in c.execute("SELECT * FROM songs"):
        saved_song = replacing(saved_song)
        my_listbox.insert("end", saved_song)
    conn.commit()
    conn.close()


def delete_from_table():
    """Thıs function enables you to delete the songs which were saved into the table."""
    conn = sqlite3.connect("song.db")
    conn.execute("CREATE TABLE IF NOT EXISTS songs (song TEXT)")

    c = conn.cursor()
    c.execute("DELETE FROM songs")
    conn.commit()
    conn.close()


my_menu = tkinter.Menu(root)
root.config(menu=my_menu)
music_menu = tkinter.Menu(my_menu)
menu = tkinter.Menu(my_menu)
my_menu.add_cascade(label="Files", menu=music_menu)
my_menu.add_cascade(label="songs", menu= menu)
music_menu.add_command(label="Add Song", command=add_song)
music_menu.add_separator()
music_menu.add_command(label="Add Many Song", command=add_many_song)
music_menu.add_separator()
music_menu.add_command(label="Exit", command=root.quit)
music_menu.add_separator()
menu.add_command(label="Save", command=save)
menu.add_separator()
menu.add_command(label="retrieve", command=retrieve_songs)
menu.add_separator()
menu.add_command(label="delete", command=delete_from_table)

add_button = ttk.Button(my_frame, text="ADD", width=8, command=add_song)
add_button.pack(side="left", ipadx=72)

delete_button = ttk.Button(my_frame, style="C.TButton", text="DELETE", width=8)
delete_button.pack(side="left", ipadx=72,)


def main_2():


    mainwindow = tkinter.Toplevel()  # creating the screen
    mainwindow.title("mp3")
    mainwindow.geometry("15000x15000")
    mainwindow.configure(background="#6F1E51")

    pygame.mixer.init()

    style = ThemedStyle(mainwindow)
    style.set_theme("arc")
    playing = False
    stopped= None

    def start_song():
        nonlocal playing
        global song
        nonlocal stopped
        # global similar

        """
       It starts the selected song.If the song is not found than it warns.
       """

        song = my_listbox.get("active")
        song = f"C:/Users/user/Downloads/{song}.mp3"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        stopped = False
        length_info()
        my_slider.config(value=0)
        playing= True
        if playing:
            get_song_image()
        print(playing,"tih is playing")
        print(song,"tih is song")




    def stop_music():
        nonlocal playing
        nonlocal stopped
        """
        It stops the selected song while the song is playing.
        It also resets the slider and both time_label and song_length_label.
        """
        if playing:
            pygame.mixer.music.stop()
            my_listbox.selection_clear("active")

            song_length_label.config(text="")
            time_label.config(text="")
            my_slider.config(value=0)
            playing= False
            stopped = True
            mainwindow.destroy()




    paused = False
    def pause():
        nonlocal paused
        """
        ıt pauses the selected song while the song is playing.
        """

        if not paused:
            pygame.mixer.music.pause()
            paused = True
        else:
            pygame.mixer.music.unpause()
            paused = False


    def next_song():
        """
        It ıs a function to pass the next song in the listbox.
        If the song is the last song in the listbox then it starts from the start of the list.
        """
        global song
        nonlocal playing
        nonlocal stopped
        try:
            next_one = my_listbox.curselection()
            num = next_one[0]
            song_length_label.config(text="")
            time_label.config(text="")
            my_slider.config(value=0)
            if (num + 1) != my_listbox.size():
                index = int(num) + 1
                song = my_listbox.get(index)
                title = f"C:/Users/user/Downloads/{song}.mp3"
                pygame.mixer.music.load(title)
                pygame.mixer.music.play(loops=0)

                my_listbox.selection_clear(0, "end")
                my_listbox.activate(index)
                my_listbox.selection_set(index, last=None)
                print(my_listbox.size())
            elif (num + 1) == my_listbox.size():
                song = my_listbox.get(0)
                title = f"C:/Users/user/Downloads/{song}.mp3"
                pygame.mixer.music.load(title)
                pygame.mixer.music.play(loops=0)
                my_listbox.selection_clear(0, "end")
                my_listbox.activate(0)
                my_listbox.selection_set(0, last=None)
            num += 1

            get_song_image()
            playing= True
            stopped = False
            print(playing,"tih is playing")
            print(song,"tih is song")

        except ValueError:
            messagebox.showwarning("Warning", "Something went wrong, please stop the current music and try again.")
        # else:
        #     messagebox.showwarning("warning", "There is no song playing currently!")
        # else:
        #     pass
        #     # similar = False


    def go_back():
        """
        It is a function to go back to the previous song.
        If you are currently playing the first song than it will start playing the last song.
        """
        global song
        nonlocal playing
        nonlocal stopped

        try:
            next_one = my_listbox.curselection()
            num = next_one[0]
            song_length_label.config(text="")
            time_label.config(text="")
            my_slider.config(value=0)

            if num != 0:

                index = int(num) - 1
                song = my_listbox.get(index)
                title = f"C:/Users/user/Downloads/{song}.mp3"
                pygame.mixer.music.load(title)
                pygame.mixer.music.play(loops=0)

                my_listbox.selection_clear(0, "end")
                my_listbox.activate(index)
                my_listbox.selection_set(index, last=None)
            elif num == 0:
                song = my_listbox.get("end")
                title = f"C:/Users/user/Downloads/{song}.mp3"
                pygame.mixer.music.load(title)
                pygame.mixer.music.play(loops=0)
                my_listbox.selection_clear(0, "end")
                my_listbox.activate("end")
                my_listbox.selection_set("end", last=None)
            num -= 1
            get_song_image()
            playing = True
            stopped= False


        except ValueError:
            messagebox.showwarning("Warning", "Something went wrong, please stop the current music and try again.")
    # else:
    # messagebox.showwarning("warning", "There is no song playing currently!")
    # else:
    #     similar = False



    def length_info():
        """
        It finds out the current time as well as the total length of the song.Then it changes them into time format
        and displays them.
        It updates the scale according to your moving.It also updates the current time which depends on the scale.
        """
        if stopped:
            return

        song_time = pygame.mixer.music.get_pos() / 1000
        song_time += 1
        title = my_listbox.get("active")
        title = f"C:/Users/user/Downloads/{title}.mp3"
        mutagen_form = MP3(title)
        global song_length
        song_length = mutagen_form.info.length
        global converted_song_length
        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
        # If the song has finished
        if int(my_slider.get()) == int(song_length):
            time_label.config(text=("Current Time: " + converted_song_length))
        elif paused % 2 != 0:
            pass

        # It means there has been no change with the slider
        elif int(my_slider.get()) == int(song_time):
            slider_position = int(song_length)
            my_slider.configure(to=slider_position, value=int(song_time))
        else:
            slider_position = int(song_length)
            my_slider.configure(to=slider_position, value=int(my_slider.get()))
            converted_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
            time_label.config(text=("Current Time: " + converted_time))
            moving = int(my_slider.get()) + 1
            my_slider.config(value=moving)
        song_length_label.config(text=("Total Song Time: " + converted_song_length))
        time_label.after(1000, length_info)


    def slide(x):
        """It updates the playing song according to your change to the scale.
        :param x: It take the value of the scale."""
        try:
            song = my_listbox.get("active")
            song = f"C:/Users/user/Downloads/{song}.mp3"

            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
        except pygame.error:
            messagebox.showwarning("Warning", "There is no song playing currently.")


    def volume(x):
        pygame.mixer.music.set_volume(volume_slider.get())
        volume_label.config(text=int(volume_slider.get() * 100))





    def get_song_image():
        global song
        try:
            song = song.replace("C:/Users/user/Downloads/", "")
            song = song.replace(".mp3", "")
            mp3 = stagger.read_tag(f"C:/Users/user/Downloads/{song}.mp3")
            by_data = mp3[stagger.id3.APIC][0].data
            im = io.BytesIO(by_data)
            imageFile = Image.open(im)
            image = imageFile.resize((600, 380), Image.ANTIALIAS)
            image_label.image= ImageTk.PhotoImage(image)
            image_label['image'] = image_label.image
        except KeyError:
            default_pic()

    def get_artist():
        global song
        try:
            song = replacing(song)
            song = song.split("-")[0]

            if "," not in song and "&" not in song :
                result = spotify.search(song) #search query
                artist_2 = result['tracks']['items'][0]['artists'][0]["external_urls"]["spotify"]
                results = spotify.artist_related_artists(artist_2)
                mine_list = []
                for p in range(19) :
                    mine_list.append(results["artists"][p]["name"])
                similar_box["values"] = mine_list

            else:
                messagebox.showwarning("warning", "Sorry, we cannot provide this feature for more than one artist.")
        except:
            messagebox.showwarning("warning", "artist name must be at the beginningRewrite the file's name!")

    combostyle = ttk.Style()
    combostyle.configure('MyCustomStyleName.TCombobox', selectbackground ='blue', fieldbackground="green",
                         background="green")


    advice = ImageTk.PhotoImage(Image.open("advice.png"))
    # similar_frame = tkinter.Frame(mainwindow)
    # similar_frame.place(x=100, y=200)
    button = tkinter.Button(mainwindow, image=advice,borderwidth=0,
                        command=get_artist)
    button.place(x=80, y=200)


    similar_box = ttk.Combobox(mainwindow,
                               values=None, style = 'MyCustomStyleName.TCombobox')
    similar_box['state'] = 'readonly'
    similar_box.place(x=100, y=300)






    image_label = tkinter.Label(mainwindow)
    image_label.place(x=380, y=0)
    def default_pic():
        imageFile = Image.open("love (2).png")
        image = imageFile.resize((600, 380), Image.ANTIALIAS)
        image_label.image= ImageTk.PhotoImage(image)
        image_label['image'] = image_label.image
    default_pic()

    # Defining the button images
    start_image = ImageTk.PhotoImage(Image.open("start (1) (1) (1) (1).png"))
    stop_image = ImageTk.PhotoImage(Image.open("stop (1) (1).png"))
    pause_image = ImageTk.PhotoImage(Image.open("pause (2).png"))
    forward_image = ImageTk.PhotoImage(Image.open("next (1).png"))
    back_image = ImageTk.PhotoImage(Image.open("previous (2).png"))

    # creating a button frame
    # button_frame = tkinter.Frame(mainwindow,)
    # button_frame.place(x=500,y=500 )

    volume_frame = tkinter.LabelFrame(mainwindow, text="Volume")
    volume_frame.place(x=1100, y = 200)

    # creating and griding the buttons
    start_button = tkinter.Button(mainwindow , image=start_image, borderwidth=0, command=start_song)
    start_button.place(x=400, y= 500)

    stop_button = tkinter.Button(mainwindow, image=stop_image, borderwidth=0 , command=stop_music)
    stop_button.place(x=500, y= 500)

    pause_button = tkinter.Button(mainwindow, image=pause_image,  borderwidth=0, command=pause)
    pause_button.place(x=600, y= 500)

    forward_button = tkinter.Button(mainwindow, image=forward_image,  borderwidth=0, command=next_song)
    forward_button.place(x=700, y=500)

    back_button = tkinter.Button(mainwindow, image=back_image, borderwidth=0, command=go_back)
    back_button.place(x=800, y=500)

    timing = tkinter.Frame(mainwindow)
    timing.place(x=400, y =420)


    my_slider = ttk.Scale(timing, from_=0, to=100, orient="horizontal", value=0, length=600, command=slide)
    my_slider.pack()

    time_label = ttk.Label(timing, text="", relief="sunken", anchor="e")
    time_label.pack()

    song_length_label = ttk.Label(timing, text="", relief="sunken", anchor="e")
    song_length_label.pack()


    volume_label = ttk.Label(volume_frame, text=50, )
    volume_label.pack(side="right")

    volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient="vertical", value=0.5, length=300, command=volume)
    volume_slider.pack(side="right")
    def artist_page():
        mainwindow_2 = tkinter.Toplevel()  # creating the screen
        mainwindow_2.title("mp3")
        mainwindow_2.geometry("15000x15000")
        mainwindow_2.configure(background="#042e07")

        #3. pencere
        WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='


        def get_wiki_link(search_term):
            """Thıs function gets allthe links of the wikipage which belongs to specified artist."""
            try:
                result = wikipedia.search(search_term, results = 1)
                print(result)
                wikipedia.set_lang('en')
                wkpage = wikipedia.WikipediaPage(title = result[0])
                print(wkpage)
                title = wkpage.title
                print(title)
                response  = requests.get(WIKI_REQUEST+title)
                print(response.text)

                json_data = json.loads(response.text)
                print(json_data)
                img_link = list(json_data['query']['pages'].values())[0]['original']['source']
                return img_link
            except:
                return 0

        def getting_image():
            """This function extracts the image link.Then ıt goes to the link an download the image into the computer."""

            cc = replacing(song)

            splitting = cc.split("-")
            print(splitting[0] + "-------------------------------------")

            wiki_image = get_wiki_link(splitting[0])

            url = wiki_image
            page = requests.get(url)

            f_ext = os.path.splitext(url)[-1]
            f_name = 'img'+ splitting[0] + "{}".format(f_ext)
            with open(f_name, 'wb') as f:
                f.write(page.content)

        pic_frame = tkinter.Frame(mainwindow_2)
        pic_frame.grid(row=7, column=10)
        image_label = tkinter.Label(pic_frame)
        image_label.pack(side="right")


        def show_image(images):
            """Thıs function resizes the image and then puts it into the Mp3 interface."""
            image = Image.open(images)
            image2 = image.resize((300, 300))

            image_label.image= ImageTk.PhotoImage(image2)

            image_label['image'] = image_label.image


        def artist():
            """
            This function  gets the artist information from wikipedia as
            a summary of the wikipedia article about the artist within 2 sentences.It also gets the image of the specified artist.
            """


            global song
            if playing:
                cc = replacing(song)

                splitting = cc.split("-")

                heading.config(text=f"                      {splitting[0]}                ")


                if "&" in splitting[0] or "," in splitting[0]:
                    again_splitted = splitting[0].split("," or "&")
                    print(again_splitted)
                    converted = tuple(again_splitted)
                    print(converted)
                    first_artist, second_artist = converted

                    try:
                        result = (wikipedia.summary(first_artist, sentences=2))
                        result2 = (wikipedia.summary(second_artist, sentences=2))
                    except:
                        artist_label.config(text="sorry, there is no artist")
                        artist_label2.config(text="")
                    else:
                        man = result.split(".")
                        sentence1 = man[0]
                        sentence2 = man[1]
                        second_artist_label2.config(text=sentence2)
                        second_artist_label.config(text=sentence1)

                        artist2 = result2.split(".")
                        sentence1 = artist2[0]
                        sentence2 = artist2[1]
                        artist_label.config(text=sentence1)
                        artist_label2.config(text=sentence2)

                else:
                    try:
                        result = (wikipedia.summary(splitting[0], sentences=4))
                    except:
                        artist_label.config(text="sorry, there is no artist")
                        artist_label2.config(text="")
                    else:
                        getting_image()
                        show_image('img'+ splitting[0] + "{}".format(".jpg"))
                        man = result.split(".")
                        sentence1 = man[0]
                        sentence2 = man[1]
                        sentence3 = man[2]
                        sentence4 = man[3]
                        artist_label.config(text=sentence1)
                        artist_label2.config(text=sentence2)
                        artist_label_3.config(text=sentence3)
                        artist_label_4.config(text=sentence4)

            else:
                messagebox.showwarning("Warning", "You need to play a song to use this property!")


        def top_tracks_func():
            global song
            song = replacing(song)
            song = song.split("-")[0]
            result = spotify.search(song)
            artist_2 = result['tracks']['items'][0]['artists'][0]["external_urls"]["spotify"]
            best_tracks = spotify.artist_top_tracks(artist_2)
            print(best_tracks)
            list_of_tracks = ((best_tracks["tracks"][i]["name"]) for i in range(len(best_tracks["tracks"])))
            list_of_tracks_2 = list(list_of_tracks)
            print(list_of_tracks_2)
            for track in list_of_tracks_2:
                my_listbox.insert("end", track)



        my_listbox = tkinter.Listbox(pic_frame, background="#910606", width=60, height=19)
        my_listbox.pack(side="right")
        top_tracks_func()
        myFont = font.Font(family="New Tegomin", size=13,)
        heading_font = font.Font(family="Josefin Sans", size=20)
        info_frame = tkinter.Frame(mainwindow_2)
        info_frame.grid(row=2, column=10)
        heading = tkinter.Label(info_frame, text="")
        heading["font"] = heading_font
        heading.pack()
        artist_label = tkinter.Label(info_frame, text="")
        artist_label["font"] = myFont
        artist_label.pack()
        artist_label2 = tkinter.Label(info_frame, text="")
        artist_label2["font"] = myFont
        artist_label2.pack()
        artist_label_3 = tkinter.Label(info_frame, text="")
        artist_label_3["font"] = myFont
        artist_label_3.pack()
        artist_label_4 = tkinter.Label(info_frame, text="")
        artist_label_4["font"] = myFont
        artist_label_4.pack()

        second_artist_label = tkinter.Label(info_frame, text="")
        second_artist_label["font"] = myFont
        second_artist_label.pack()
        second_artist_label2 = tkinter.Label(info_frame, text="")
        second_artist_label2["font"] = myFont
        second_artist_label2.pack()


        artist()
        mainwindow_2.mainloop()






    menu_1 = tkinter.Menu(mainwindow)
    mainwindow.config(menu=menu_1)
    artist_menu = tkinter.Menu(menu_1)
    menu_1.add_cascade(label="Artist", menu=artist_menu)

    artist_menu.add_command(label="About artist", command=artist_page)

    mainwindow.mainloop()

new_widget = ttk.Button(my_frame, style="C.TButton", text="PLAY THE SONG", width=8, command=main_2)
new_widget.pack(side="right", ipadx=72, )




root.mainloop()





# def func():
#     """
#     This function gets information about the specified singer.It gets the image as well.
#     """
#     try:
#         link = get_wiki_link(en.get())
#
#         page = requests.get(link)
#
#         f_ext = os.path.splitext(link)[-1]
#         print(f_ext)
#         f_name = 'img'+ en.get() + "{}".format(f_ext)
#         with open(f_name, 'wb') as f:
#             f.write(page.content)
#         show_image('img'+ en.get() + "{}".format(f_ext))
#
#         result = wikipedia.summary(en.get(), sentences=2)
#         splitted = result.split(".")
#         sentence = splitted[0]
#         sentence2 = splitted[1]
#         artist_label.config(text=sentence)
#         artist_label2.config(text=sentence2)
#     except:
#         messagebox.showwarning("warning", "Please remove the info and try again!")


# def remove_info():
#
#     """
#     This function removes the information.
#
#     """
#     artist_label.config(text="")
#     artist_label2.config(text="")
#     second_artist_label.config(text="")
#     second_artist_label2.config(text="")
#     image_label["image"] = ""
#     artist_button.deselect()
#
#
#


