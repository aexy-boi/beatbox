import os  
import sys  
import time  
import yt_dlp as ytdl  
import eyed3  
from rich.console import Console  
from rich.prompt import Prompt  
import subprocess  

# Setup  
console = Console()  
BASE_DIR = os.path.expanduser("~/Beatbox_Music")  # Updated folder name
LIKED_DIR = os.path.join(BASE_DIR, "liked_songs")  
ALL_SONGS_DIR = os.path.join(BASE_DIR, "all_songs")  

# Ensure directories exist  
os.makedirs(LIKED_DIR, exist_ok=True)  
os.makedirs(ALL_SONGS_DIR, exist_ok=True)  

# Core Functions  
def download_song(url, folder="all_songs"):  
    try:  
        folder_path = os.path.join(BASE_DIR, folder)  
        os.makedirs(folder_path, exist_ok=True)  
        ydl_opts = {  
            'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),  
            'format': 'bestaudio/best',  
            'postprocessors': [{  
                'key': 'FFmpegExtractAudio',  
                'preferredcodec': 'mp3',  
                'preferredquality': '192',  
            }],  
            'noplaylist': True,  
            'quiet': False,  
        }  
        with ytdl.YoutubeDL(ydl_opts) as ydl:  
            info_dict = ydl.extract_info(url, download=True)  
            title = info_dict.get('title', 'song')  
            filename = f"{title}.mp3"  
            filepath = os.path.join(folder_path, filename)  

        # Add metadata  
        audio = eyed3.load(filepath)  
        if audio and audio.tag is None:  
            audio.initTag()  
        if audio:  
            audio.tag.title = info_dict.get('title')  
            audio.tag.artist = info_dict.get('uploader')  
            audio.tag.save()  

        return filepath  
    except Exception as e:  
        console.print(f"[red]Error downloading song: {e}[/red]")  
        return None  

def like_song(song_path):  
    if not os.path.isfile(song_path):  
        console.print("[red]Song file not found.[/red]")  
        return  
    filename = os.path.basename(song_path)  
    new_name = filename if not os.path.exists(os.path.join(LIKED_DIR, filename)) else f"{int(time.time())}_{filename}"  
    liked_path = os.path.join(LIKED_DIR, new_name)  
    os.rename(song_path, liked_path)  
    console.print(f"[green]❤️ Added to favorites![/green]")  

def play_audio(path):  
    subprocess.run(["mpv", path])  

# Menus  
def main_menu():  
    while True:  
        console.print("\n[bold cyan]BEATBOX[/bold cyan]")  # Updated name
        choice = Prompt.ask(  
            "[1] Search & Play\n[2] Download\n[3] Library\n[4] Settings\n[5] Exit",  
            choices=["1", "2", "3", "4", "5"]  
        )  

        if choice == "1": search_menu()  
        elif choice == "2": download_menu()  
        elif choice == "3": library_menu()  
        elif choice == "4": settings_menu()  
        elif choice == "5": sys.exit()  

def search_menu():  
    query = Prompt.ask("🎵 Search song")  
    ydl_opts = {  
        'quiet': True,  
        'extractaudio': True,  
        'noplaylist': True,  
    }  
    with ytdl.YoutubeDL(ydl_opts) as ydl:  
        info = ydl.extract_info(f"ytsearch5:{query}", download=False)  
        results = info.get("entries", [])  

    if not results:  
        console.print("[red]No results found.[/red]")  
        return  

    for i, vid in enumerate(results):  
        duration = f"{vid['duration'] // 60}:{vid['duration'] % 60:02d}"  
        console.print(f"[yellow]{i+1}.[/yellow] {vid['title']} ({duration})")  

    index = int(Prompt.ask("Select", choices=[str(i+1) for i in range(len(results))])) - 1  
    video = results[index]  

    console.print(f"\n[bold]Now Playing:[/bold] {video['title']}")  
    console.print("Press [red]'q'[/red] to quit, [green]'l'[/green] to like")  

    # Fix: Extract the best audio stream URL from formats  
    with ytdl.YoutubeDL({'quiet': True}) as ydl:  
        full_info = ydl.extract_info(video['webpage_url'], download=False)  
          
        # Extract the best audio stream URL  
        stream_url = None  
        for fmt in full_info.get("formats", []):  
            if fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":  
                stream_url = fmt.get("url")  
                break  

        if not stream_url:  
            console.print("[red]Error: No audio stream found.[/red]")  
            return  # return inside the function if no stream is found  

    play_audio(stream_url)  

    while True:  
        cmd = Prompt.ask("", choices=["q", "l"], default="q")  
        if cmd == "l":  
            song_path = download_song(video['webpage_url'])  
            if song_path:  
                like_song(song_path)  
        if cmd == "q":  
            break  

def download_menu():  
    url = Prompt.ask("Enter YouTube URL to download")  
    song_path = download_song(url)  
    if song_path:  
        console.print(f"[green]Download completed![/green] Saved to: {song_path}")  
    else:  
        console.print("[red]Download failed.[/red]")  

def library_menu():  
    console.print("\n[bold cyan]Library[/bold cyan]")  
    console.print(f"Liked Songs: {len(os.listdir(LIKED_DIR))}")  
    console.print(f"All Songs: {len(os.listdir(ALL_SONGS_DIR))}")  

    choice = Prompt.ask(  
        "[1] View Liked Songs\n[2] View All Songs\n[3] Back",  
        choices=["1", "2", "3"]  
    )  

    if choice == "1": view_library(LIKED_DIR)  
    elif choice == "2": view_library(ALL_SONGS_DIR)  

def view_library(library_dir):  
    songs = os.listdir(library_dir)  
    if not songs:  
        console.print("[red]No songs found.[/red]")  
        return  

    for i, song in enumerate(songs):  
        console.print(f"[yellow]{i+1}.[/yellow] {song}")  

    choice = Prompt.ask("Select song or [b]Back", choices=[str(i+1) for i in range(len(songs))] + ["b"])  
    if choice == "b":  
        return  
    song_path = os.path.join(library_dir, songs[int(choice)-1])  
    play_audio(song_path)  

def settings_menu():  
    console.print("[yellow]Settings[/yellow]")  
    choice = Prompt.ask(  
        "[1] Change download folder\n[2] Toggle metadata tagging\n[3] Back",  
        choices=["1", "2", "3"]  
    )  
    if choice == "1":  
        change_download_folder()  
    elif choice == "2":  
        toggle_metadata_tagging()  

def change_download_folder():  
    global BASE_DIR, LIKED_DIR, ALL_SONGS_DIR  
    new_folder = Prompt.ask("Enter new folder path")  
    BASE_DIR = os.path.expanduser(new_folder)  
    LIKED_DIR = os.path.join(BASE_DIR, "liked_songs")  
    ALL_SONGS_DIR = os.path.join(BASE_DIR, "all_songs")  
    os.makedirs(LIKED_DIR, exist_ok=True)  
    os.makedirs(ALL_SONGS_DIR, exist_ok=True)  
    console.print(f"[green]Download folder changed to {BASE_DIR}[/green]")  

def toggle_metadata_tagging():  
    # Placeholder toggle  
    console.print("[green]Metadata tagging toggle is not implemented yet.[/green]")  

if __name__ == "__main__":  
    main_menu()
