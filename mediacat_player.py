import tkinter as tk
from tkinter import filedialog, font, ttk, messagebox
import pygame.mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError, ID3, APIC
from mutagen.wave import WAVE
from mutagen.flac import FLAC
from PIL import Image, ImageTk
import os
import sys
import threading
import time
import random
import io
import configparser

# --- Színtéma definíciók (Angol kulcsokkal) ---
THEME_DEFINITIONS = {
    "Minecraft Green": {
        "bg_main": "#1a1a1a",      # Fő ablak háttér
        "fg_accent": "#38b438",    # Minecraft zöld (gombok, progress bar)
        "bg_dark_frame": "#282828", # Sötétszürke keretek
        "text_light": "white",     # Világos szöveg
        "text_dark": "black",      # Sötét szöveg (pl. zöld gombon)
        "listbox_bg": "#282828",
        "listbox_fg": "white",
        "listbox_select_bg": "#38b438",
        "listbox_select_fg": "black",
        "entry_bg": "black",
        "entry_fg": "#38b438",
        "entry_insert": "#38b438",
        "highlight_color": "#38b438", # Entry highlight, scrollbar
        "progressbar_trough": "black",
        "scrollbar_bg": "#38b438",
        "scrollbar_trough": "#282828"
    },
    "Black & White": {
        "bg_main": "#000000",
        "fg_accent": "#ffffff",
        "bg_dark_frame": "#333333",
        "text_light": "white",
        "text_dark": "black",
        "listbox_bg": "#333333",
        "listbox_fg": "white",
        "listbox_select_bg": "#555555",
        "listbox_select_fg": "white",
        "entry_bg": "#000000",
        "entry_fg": "white",
        "entry_insert": "white",
        "highlight_color": "#cccccc",
        "progressbar_trough": "#555555",
        "scrollbar_bg": "#cccccc",
        "scrollbar_trough": "#333333"
    },
    "Sea Blue": {
        "bg_main": "#1a2a3a",
        "fg_accent": "#4a90e2", # Kék
        "bg_dark_frame": "#2a3a4a",
        "text_light": "#e0f2f7",
        "text_dark": "black",
        "listbox_bg": "#2a3a4a",
        "listbox_fg": "#e0f2f7",
        "listbox_select_bg": "#4a90e2",
        "listbox_select_fg": "white",
        "entry_bg": "#1a2a3a",
        "entry_fg": "#4a90e2",
        "entry_insert": "#4a90e2",
        "highlight_color": "#4a90e2",
        "progressbar_trough": "#3a4a5a",
        "scrollbar_bg": "#4a90e2",
        "scrollbar_trough": "#2a3a4a"
    }
}

# --- Nyelvi definíciók ---
LANGUAGES = {
    "Magyar": {
        "MediaCat - Control Panel": "MediaCat - Vezérlőpult",
        "MediaCat - Playlist": "MediaCat - Lejátszási lista",
        "MediaCat - Album Art": "MediaCat - Albumkép",
        "MediaCat - Controls": "MediaCat - Vezérlők",
        "MediaCat - Settings": "MediaCat - Beállítások",
        "Playlist": "Lejátszási lista",
        "No song playing": "Nincs lejátszás",
        "Volume:": "Hangerő:",
        "Browse": "Tallózás",
        "Save": "Mentés",
        "Load": "Betöltés",
        "Settings": "Beállítások",
        "Choose Theme:": "Válassz témát:",
        "Apply & Save": "Alkalmaz & Mentés",
        "Theme successfully saved and applied!": "Téma sikeresen mentve és alkalmazva!",
        "Error": "Hiba",
        "This song is already in the playlist:": "Ez a dal már szerepel a lejátszási listán:",
        "Failed to load file:": "Nem sikerült betölteni a fájlt:",
        "No song selected for playback.": "Nincs kiválasztott dal a lejátszáshoz.",
        "Playlist is empty. Nothing to save.": "A lejátszási lista üres. Nincs mit menteni.",
        "Playlist successfully saved!": "Lejátszási lista sikeresen elmentve!",
        "Error saving playlist:": "Hiba a lejátszási lista mentésekor:",
        "Failed to load file from playlist:": "Nem sikerült betölteni a fájlt a lejátszási listából:",
        "File not found:": "A fájl nem található:",
        "Playlist successfully loaded!": "Lejátszási lista sikeresen betöltve!",
        "Error loading playlist:": "Hiba a lejátszási lista betöltésekor:",
        "Choose Language:": "Válassz nyelvet:",
        "Language successfully saved and applied!": "Nyelv sikeresen mentve és alkalmazva!",
        "Error loading default album art:": "Hiba az alapértelmezett albumkép betöltésekor:",
        "Sound loading error:": "Hang betöltési hiba:",
        "Open Source Software": "Nyílt forráskódú szoftver",
        "Developed by MediaCat Inc.": "Fejlesztette a MediaCat Inc.",
        "Close process in Task Manager if app freezes.": "Zárd be a folyamatot a Feladatkezelőben, ha az alkalmazás lefagy.",
        "Error setting window icon:": "Hiba az ablak ikon beállításakor:",
        # Új téma fordítások
        "Minecraft Green": "Minecraft Zöld",
        "Black & White": "Fekete & Fehér",
        "Sea Blue": "Tenger Kék",
    },
    "English": {
        "MediaCat - Control Panel": "MediaCat - Control Panel",
        "MediaCat - Playlist": "MediaCat - Playlist",
        "MediaCat - Album Art": "MediaCat - Album Art",
        "MediaCat - Controls": "MediaCat - Controls",
        "MediaCat - Settings": "MediaCat - Settings",
        "Playlist": "Playlist",
        "No song playing": "No song playing",
        "Volume:": "Volume:",
        "Browse": "Browse",
        "Save": "Save",
        "Load": "Load",
        "Settings": "Settings",
        "Choose Theme:": "Choose Theme:",
        "Apply & Save": "Apply & Save",
        "Theme successfully saved and applied!": "Theme successfully saved and applied!",
        "Error": "Error",
        "This song is already in the playlist:": "This song is already in the playlist:",
        "Failed to load file:": "Failed to load file:",
        "No song selected for playback.": "No song selected for playback.",
        "Playlist is empty. Nothing to save.": "Playlist is empty. Nothing to save.",
        "Playlist successfully saved!": "Playlist successfully saved!",
        "Error saving playlist:": "Error saving playlist:",
        "Failed to load file from playlist:": "Failed to load file from playlist:",
        "File not found:": "File not found:",
        "Playlist successfully loaded!": "Playlist successfully loaded!",
        "Error loading playlist:": "Error loading playlist:",
        "Choose Language:": "Choose Language:",
        "Language successfully saved and applied!": "Language successfully saved and applied!",
        "Error loading default album art:": "Error loading default album art:",
        "Sound loading error:": "Sound loading error:",
        "Open Source Software": "Open Source Software",
        "Developed by MediaCat Inc.": "Developed by MediaCat Inc.",
        "Close process in Task Manager if app freezes.": "Close process in Task Manager if app freezes.",
        "Error setting window icon:": "Error setting window icon:",
        # Új téma fordítások
        "Minecraft Green": "Minecraft Green",
        "Black & White": "Black & White",
        "Sea Blue": "Sea Blue",
    }
}

# Globális változó az aktuális fordítási szótárhoz
current_translation_dict = {} 

def _(text):
    """Fordítási függvény."""
    return current_translation_dict.get(text, text)

# --- Segéd osztály a stílusokhoz ---
class CustomStyle:
    def __init__(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Betűtípusok definíciója
        try:
            self.MINECRAFT_FONT_LARGE = font.Font(family="Minecraft Regular", size=18)
            self.MINECRAFT_FONT_MEDIUM = font.Font(family="Minecraft Regular", size=14)
            self.MINECRAFT_FONT_SMALL = font.Font(family="Arial", size=10)
        except:
            self.MINECRAFT_FONT_LARGE = font.Font(family="Arial", size=18)
            self.MINECRAFT_FONT_MEDIUM = font.Font(family="Arial", size=14)
            self.MINECRAFT_FONT_SMALL = font.Font(family="Arial", size=10)

        # Kezdeti színek (ezeket felülírja a set_theme)
        self.colors = THEME_DEFINITIONS["Minecraft Green"] # Alapértelmezett téma
        self.apply_ttk_styles()
        
    def set_theme(self, theme_name):
        if theme_name in THEME_DEFINITIONS:
            self.colors = THEME_DEFINITIONS[theme_name]
            self.apply_ttk_styles()

    def apply_ttk_styles(self):
        self.style.configure("TFrame", background=self.colors["bg_main"])
        self.style.configure("TLabel", background=self.colors["bg_main"], foreground=self.colors["text_light"], font=self.MINECRAFT_FONT_SMALL)
        
        self.style.configure("TButton", background=self.colors["fg_accent"], foreground=self.colors["text_dark"], font=self.MINECRAFT_FONT_MEDIUM,
                                relief="flat", borderwidth=0, focusthickness=0,
                                activebackground=self.colors["fg_accent"], activeforeground=self.colors["text_dark"],
                                padding=[5,5,5,5])
        self.style.map("TButton", background=[("active", self.colors["fg_accent"]), ("pressed", self.colors["fg_accent"])])

        self.style.configure("Green.Horizontal.TProgressbar",
                                foreground=self.colors["fg_accent"], background=self.colors["fg_accent"],
                                troughcolor=self.colors["progressbar_trough"], bordercolor=self.colors["fg_accent"],
                                lightcolor=self.colors["fg_accent"], darkcolor=self.colors["fg_accent"],
                                relief="flat", thickness=10)
        
        self.style.configure("TRadiobutton", background=self.colors["bg_dark_frame"], foreground=self.colors["text_light"],
                             font=self.MINECRAFT_FONT_SMALL,
                             indicatorcolor=self.colors["fg_accent"],
                             selectcolor=self.colors["bg_dark_frame"])
        self.style.map("TRadiobutton", background=[("active", self.colors["bg_dark_frame"])])


# --- Ablak osztályok ---

class PlaylistWindow:
    def __init__(self, master, player_app, custom_style):
        self.master = master
        self.player_app = player_app
        self.custom_style = custom_style
        self.window = tk.Toplevel(master)
        self.window.geometry("350x600")
        self.window.minsize(300, 400)
        self.window.withdraw()

        self.title_label = tk.Label(self.window, font=self.custom_style.MINECRAFT_FONT_LARGE)
        self.title_label.pack(pady=10)

        self.search_entry = tk.Entry(self.window, font=self.custom_style.MINECRAFT_FONT_SMALL,
                                     bd=0, relief="flat", highlightthickness=1)
        self.search_entry.pack(pady=5, padx=10, fill="x")
        self.search_entry.bind("<KeyRelease>", self.player_app.filter_playlist)

        self.playlist_listbox_frame = tk.Frame(self.window, bd=2, relief="solid", highlightthickness=1)
        self.playlist_listbox_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.playlist_listbox = tk.Listbox(self.playlist_listbox_frame, font=self.custom_style.MINECRAFT_FONT_SMALL, bd=0, highlightthickness=0, activestyle="none")
        self.playlist_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.playlist_listbox.bind("<Double-Button-1>", self.player_app.play_selected_song)

        self.scrollbar = tk.Scrollbar(self.playlist_listbox_frame, orient="vertical", command=self.playlist_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.playlist_listbox.config(yscrollcommand=self.scrollbar.set)

        self.playlist_actions_frame = tk.Frame(self.window)
        self.playlist_actions_frame.pack(pady=10, padx=10, fill="x")

        self.browse_button = ttk.Button(self.playlist_actions_frame, command=self.player_app.browse_files)
        self.browse_button.pack(side="left", expand=True, padx=2)

        self.save_playlist_button = ttk.Button(self.playlist_actions_frame, command=self.player_app.save_playlist)
        self.save_playlist_button.pack(side="left", expand=True, padx=2)

        self.load_playlist_button = ttk.Button(self.playlist_actions_frame, command=self.player_app.load_playlist)
        self.load_playlist_button.pack(side="left", expand=True, padx=2)

        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.update_ui() # Kezdeti UI frissítés

    def hide_window(self):
        self.window.withdraw()

    def show_window(self):
        self.window.deiconify()

    def update_ui(self):
        colors = self.custom_style.colors
        self.window.configure(bg=colors["bg_dark_frame"])
        self.window.title(_("MediaCat - Playlist")) # Ablak cím frissítése
        
        self.title_label.config(text=_("Playlist"), bg=colors["bg_dark_frame"], fg=colors["fg_accent"])
        
        self.search_entry.config(bg=colors["entry_bg"], fg=colors["entry_fg"],
                                 insertbackground=colors["entry_insert"], highlightbackground=colors["highlight_color"])
        
        self.playlist_listbox_frame.config(bg=colors["bg_dark_frame"], highlightbackground=colors["highlight_color"])
        self.playlist_listbox.config(bg=colors["listbox_bg"], fg=colors["listbox_fg"],
                                     selectbackground=colors["listbox_select_bg"], selectforeground=colors["listbox_select_fg"])
        
        self.scrollbar.config(troughcolor=colors["scrollbar_trough"], bg=colors["scrollbar_bg"], activebackground=colors["scrollbar_bg"])
        
        self.playlist_actions_frame.config(bg=colors["bg_dark_frame"])
        self.browse_button.config(text=_("Browse"))
        self.save_playlist_button.config(text=_("Save"))
        self.load_playlist_button.config(text=_("Load"))


class AlbumArtWindow:
    def __init__(self, master, player_app, custom_style):
        self.master = master
        self.player_app = player_app
        self.custom_style = custom_style
        self.window = tk.Toplevel(master)
        self.window.geometry("400x450")
        self.window.minsize(300, 350)
        self.window.withdraw()

        self.album_art_canvas = tk.Canvas(self.window, bg="black", bd=0, highlightthickness=0)
        self.album_art_canvas.pack(pady=20, fill="both", expand=True)
        self.album_art_id = None

        self.song_title_label = tk.Label(self.window, font=self.custom_style.MINECRAFT_FONT_LARGE, wraplength=350)
        self.song_title_label.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.update_ui() # Kezdeti UI frissítés

    def hide_window(self):
        self.window.withdraw()

    def show_window(self):
        self.window.deiconify()

    def update_ui(self):
        colors = self.custom_style.colors
        self.window.configure(bg=colors["bg_main"])
        self.window.title(_("MediaCat - Album Art")) # Ablak cím frissítése
        self.song_title_label.config(text=_("No song playing"), bg=colors["bg_main"], fg=colors["text_light"])
        # A vászon háttére fekete marad, mert az az albumkép háttere.


class PlayerControlsWindow:
    def __init__(self, master, player_app, custom_style):
        self.master = master
        self.player_app = player_app
        self.custom_style = custom_style
        self.window = tk.Toplevel(master)
        self.window.geometry("700x120")
        self.window.minsize(500, 100)
        self.window.withdraw()

        self.control_buttons_frame = tk.Frame(self.window)
        self.control_buttons_frame.pack(side="left", fill="y", padx=20, pady=5) 

        self.prev_button = ttk.Button(self.control_buttons_frame, text="⏮️", command=self.player_app.play_previous)
        self.prev_button.pack(side="left", padx=5)

        self.play_pause_button = ttk.Button(self.control_buttons_frame, text="▶️", command=self.player_app.toggle_play_pause)
        self.play_pause_button.pack(side="left", padx=5)

        self.stop_button = ttk.Button(self.control_buttons_frame, text="⏹️", command=self.player_app.stop_song)
        self.stop_button.pack(side="left", padx=5)

        self.next_button = ttk.Button(self.control_buttons_frame, text="⏭️", command=self.player_app.play_next)
        self.next_button.pack(side="left", padx=5)

        self.repeat_button = ttk.Button(self.control_buttons_frame, text="🔁", command=self.player_app.toggle_repeat)
        self.repeat_button.pack(side="left", padx=5)

        self.progress_frame = tk.Frame(self.window)
        self.progress_frame.pack(side="left", fill="both", expand=True, padx=20, pady=5) 

        self.time_label = tk.Label(self.progress_frame, text="0:00 / 0:00", font=self.custom_style.MINECRAFT_FONT_SMALL)
        self.time_label.pack(side="top", anchor="w", padx=5)

        self.progress_bar = ttk.Progressbar(self.progress_frame, style="Green.Horizontal.TProgressbar",
                                             orient="horizontal", mode="determinate",
                                             variable=self.player_app.progress_var) # Hozzáadtuk a variable paramétert
        self.progress_bar.pack(side="top", fill="x", expand=True, padx=5)
        self.progress_bar.bind("<Button-1>", self.player_app.seek_song)

        self.volume_frame = tk.Frame(self.window)
        self.volume_frame.pack(side="right", fill="y", padx=20, pady=5) 

        self.volume_label = tk.Label(self.volume_frame, font=self.custom_style.MINECRAFT_FONT_SMALL)
        self.volume_label.pack(side="left", padx=5)

        self.volume_scale = tk.Scale(self.volume_frame, from_=0, to=1, resolution=0.01, orient="horizontal",
                                     command=self.player_app.set_volume, showvalue=0,
                                     sliderrelief="flat", bd=0, length=100)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side="left", padx=5)

        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.update_ui() # Kezdeti UI frissítés

    def hide_window(self):
        self.window.withdraw()

    def show_window(self):
        self.window.deiconify()

    def update_ui(self):
        colors = self.custom_style.colors
        self.window.configure(bg=colors["bg_dark_frame"])
        self.window.title(_("MediaCat - Controls")) # Ablak cím frissítése
        self.control_buttons_frame.config(bg=colors["bg_dark_frame"])
        self.progress_frame.config(bg=colors["bg_dark_frame"])
        self.volume_frame.config(bg=colors["bg_dark_frame"])
        
        self.time_label.config(bg=colors["bg_dark_frame"], fg=colors["text_light"])
        self.volume_label.config(text=_("Volume:"), bg=colors["bg_dark_frame"], fg=colors["text_light"])
        
        self.volume_scale.config(bg=colors["bg_dark_frame"], fg=colors["text_light"],
                                 highlightbackground=colors["bg_dark_frame"], troughcolor=colors["progressbar_trough"])


class SettingsWindow:
    def __init__(self, master, player_app, custom_style):
        self.master = master
        self.player_app = player_app
        self.custom_style = custom_style
        self.window = tk.Toplevel(master)
        self.window.geometry("300x300") # Növeltük a méretet a nyelvi beállítás miatt
        self.window.resizable(False, False)
        self.window.withdraw()

        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Témaszelekció
        self.theme_label = tk.Label(self.window, font=self.custom_style.MINECRAFT_FONT_MEDIUM)
        self.theme_label.pack(pady=10)

        self.theme_selection_frame = tk.Frame(self.window)
        self.theme_selection_frame.pack(pady=5)

        # A selected_theme StringVar most az angol kulcsot tárolja
        self.selected_theme = tk.StringVar(value=self.player_app.current_theme_name)
        
        # A rádiógombok szövege most a fordítási függvényen keresztül jön
        for theme_internal_name in THEME_DEFINITIONS.keys():
            rb = ttk.Radiobutton(self.theme_selection_frame, text=_(theme_internal_name), variable=self.selected_theme,
                                 value=theme_internal_name, command=self.apply_theme_preview)
            rb.pack(anchor="w", padx=10, pady=2)
        
        # Nyelv szelekció
        self.language_label = tk.Label(self.window, font=self.custom_style.MINECRAFT_FONT_MEDIUM)
        self.language_label.pack(pady=10)

        self.language_selection_frame = tk.Frame(self.window)
        self.language_selection_frame.pack(pady=5)

        self.selected_language = tk.StringVar(value=self.player_app.current_language_name)

        for lang_name in LANGUAGES.keys():
            rb = ttk.Radiobutton(self.language_selection_frame, text=lang_name, variable=self.selected_language,
                                 value=lang_name, command=self.apply_language_preview)
            rb.pack(anchor="w", padx=10, pady=2)

        self.apply_button = ttk.Button(self.window, command=self.save_and_apply_settings)
        self.apply_button.pack(pady=15)

        self.update_ui() # Kezdeti UI frissítés

    def hide_window(self):
        self.window.withdraw()

    def show_window(self):
        self.selected_theme.set(self.player_app.current_theme_name) # Frissíti a kijelölt rádiógombot
        self.selected_language.set(self.player_app.current_language_name) # Frissíti a kijelölt nyelvet
        self.update_ui() # Frissíti az ablak szövegeit a helyes nyelvvel
        self.window.deiconify()

    def apply_theme_preview(self):
        self.player_app.set_theme(self.selected_theme.get())

    def apply_language_preview(self):
        self.player_app.set_language(self.selected_language.get())

    def save_and_apply_settings(self):
        self.player_app.set_theme(self.selected_theme.get())
        self.player_app.set_language(self.selected_language.get()) # Alkalmazza a kiválasztott nyelvet
        self.player_app.save_settings()
        messagebox.showinfo(_("Settings"), _("Theme and language successfully saved and applied!")) # Fordított üzenet
        self.hide_window()

    def update_ui(self):
        colors = self.custom_style.colors
        self.window.configure(bg=colors["bg_dark_frame"])
        self.window.title(_("MediaCat - Settings")) # Ablak cím frissítése
        
        self.theme_label.config(text=_("Choose Theme:"), bg=colors["bg_dark_frame"], fg=colors["text_light"])
        self.theme_selection_frame.config(bg=colors["bg_dark_frame"])
        
        # A rádiógombok szövegének frissítése (fontos, hogy itt újrafordítsuk őket)
        for i, theme_internal_name in enumerate(THEME_DEFINITIONS.keys()):
            rb = self.theme_selection_frame.winfo_children()[i]
            rb.config(text=_(theme_internal_name))

        self.language_label.config(text=_("Choose Language:"), bg=colors["bg_dark_frame"], fg=colors["text_light"])
        self.language_selection_frame.config(bg=colors["bg_dark_frame"])

        self.apply_button.config(text=_("Apply & Save")) # Gomb szövegének frissítése


class MediaCatPlayer:
    def __init__(self, master):
        self.master = master
        master.resizable(False, False)
        
        # Beállítások betöltése
        self.config = configparser.ConfigParser()
        self.settings_file = "mediacat_settings.ini"
        self.load_settings()

        # Nyelvi szótár beállítása a betöltött nyelv alapján
        self.set_language_dict(self.current_language_name) 

        self.custom_style = CustomStyle()
        self.custom_style.set_theme(self.current_theme_name) # Itt már az angol kulcsot kapja
        
        self.master.configure(bg=self.custom_style.colors["bg_main"])

        pygame.mixer.init() 
        
        self.block_break_sound = None
        self.glass_breaking_sound = None
        
        # Hangfájlok betöltése
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            block_break_path = os.path.join(base_path, "block_break.wav")
            glass_breaking_path = os.path.join(base_path, "glass_breaking.wav")
            if os.path.exists(block_break_path):
                self.block_break_sound = pygame.mixer.Sound(block_break_path)
            if os.path.exists(glass_breaking_path):
                self.glass_breaking_sound = pygame.mixer.Sound(glass_breaking_path)
        except pygame.error as e:
            messagebox.showerror(_("Error"), _(f"Sound loading error: {e}"))


        self.playlist = []
        self.current_song_index = -1
        self.paused = False
        self.repeat_mode = False
        self.album_photo = None
        self.is_closing = False
        
        self.progress_var = tk.DoubleVar() # Létrehoztuk a progress var-t

        # Ablakok inicializálása
        self.playlist_window = PlaylistWindow(master, self, self.custom_style)
        self.album_art_window = AlbumArtWindow(master, self, self.custom_style)
        self.player_controls_window = PlayerControlsWindow(master, self, self.custom_style)
        self.settings_window = SettingsWindow(master, self, self.custom_style)

        # Hivatkozások a widgetekre
        self.playlist_listbox = self.playlist_window.playlist_listbox
        self.search_entry = self.playlist_window.search_entry
        self.song_title_label = self.album_art_window.song_title_label
        self.album_art_canvas = self.album_art_window.album_art_canvas
        self.play_pause_button = self.player_controls_window.play_pause_button
        self.repeat_button = self.player_controls_window.repeat_button
        self.time_label = self.player_controls_window.time_label
        self.progress_bar = self.player_controls_window.progress_bar # Ez már a variable-lel van létrehozva
        self.volume_scale = self.player_controls_window.volume_scale

        self.control_panel_frame = tk.Frame(master)
        self.control_panel_frame.pack(pady=10, expand=True) 

        ttk.Button(self.control_panel_frame, text=_("Playlist"), command=self.playlist_window.show_window).pack(side="left", padx=5)
        ttk.Button(self.control_panel_frame, text=_("Album Art"), command=self.album_art_window.show_window).pack(side="left", padx=5)
        ttk.Button(self.control_panel_frame, text=_("Controls"), command=self.player_controls_window.show_window).pack(side="left", padx=5)
        ttk.Button(self.control_panel_frame, text="⚙️", command=self.settings_window.show_window).pack(side="left", padx=5) # Settings emoji

        self.update_time()
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_default_album_art()
        self.update_all_ui() # Első indításkor frissíti az összes UI elemet

    def set_language_dict(self, lang_name):
        global current_translation_dict
        if lang_name in LANGUAGES:
            current_translation_dict = LANGUAGES[lang_name]
        else:
            current_translation_dict = LANGUAGES["English"] # Fallback

    def load_settings(self):
        self.config.read(self.settings_file)
        # Az alapértelmezett téma neve mostantól angol kulcs
        self.current_theme_name = self.config.get('Settings', 'theme', fallback="Minecraft Green")
        if self.current_theme_name not in THEME_DEFINITIONS:
            self.current_theme_name = "Minecraft Green"
        
        self.current_language_name = self.config.get('Settings', 'language', fallback="Magyar")
        if self.current_language_name not in LANGUAGES:
            self.current_language_name = "Magyar"

    def save_settings(self):
        if not self.config.has_section('Settings'):
            self.config.add_section('Settings')
        self.config.set('Settings', 'theme', self.current_theme_name) # Itt is angol kulcsot mentünk
        self.config.set('Settings', 'language', self.current_language_name)
        with open(self.settings_file, 'w') as f:
            self.config.write(f)

    def set_theme(self, theme_name):
        self.current_theme_name = theme_name
        self.custom_style.set_theme(theme_name)
        self.update_all_ui() # Frissíti az összes ablak színét és szövegét

    def set_language(self, lang_name):
        self.current_language_name = lang_name
        self.set_language_dict(lang_name) # Frissíti a globális fordítási szótárt
        self.update_all_ui() # Frissíti az összes ablak színét és szövegét

    def update_all_ui(self):
        colors = self.custom_style.colors
        self.master.configure(bg=colors["bg_main"])
        self.master.title(_("MediaCat - Control Panel")) # Fő ablak cím frissítése
        self.control_panel_frame.config(bg=colors["bg_main"])

        # Frissíti a fő panel gombjait
        self.control_panel_frame.winfo_children()[0].config(text=_("Playlist"))
        self.control_panel_frame.winfo_children()[1].config(text=_("Album Art"))
        self.control_panel_frame.winfo_children()[2].config(text=_("Controls"))
        self.control_panel_frame.winfo_children()[3].config(text="⚙️") # Settings emoji marad

        # Frissíti az összes ablak UI-ját
        self.playlist_window.update_ui()
        self.album_art_window.update_ui()
        self.player_controls_window.update_ui()
        self.settings_window.update_ui()


    def play_block_break_sound(self):
        if self.block_break_sound:
            self.block_break_sound.play()

    def play_glass_breaking_sound(self):
        if self.glass_breaking_sound:
            self.glass_breaking_sound.play()

    def show_error_message(self, message):
        messagebox.showerror(_("Error"), message)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac"), (_("All Files"), "*.*")]
        )
        if file_paths:
            self.add_songs_to_playlist(file_paths)

    def add_songs_to_playlist(self, file_paths):
        new_songs_added = False
        for path in file_paths:
            if path in [song[0] for song in self.playlist]:
                self.show_error_message(_(f"This song is already in the playlist: {os.path.basename(path)}"))
                continue
            
            length, album_art, title = self.get_file_metadata(path)
            if length > 0 or path.lower().endswith((".mp3", ".wav", ".flac")):
                self.playlist.append((path, length, album_art, title))
                self.playlist_listbox.insert(tk.END, title)
                new_songs_added = True
            else:
                self.show_error_message(_(f"Failed to load file: {os.path.basename(path)}"))

        if new_songs_added and not pygame.mixer.music.get_busy() and self.current_song_index == -1:
            self.play_song(0)
            self.playlist_listbox.selection_set(0)
            self.playlist_listbox.see(0)

    def get_file_metadata(self, file_path):
        length = 0
        album_art = None
        title = os.path.basename(file_path)

        try:
            if file_path.lower().endswith(".mp3"):
                audio = MP3(file_path)
                length = audio.info.length
                
                try:
                    tags = ID3(file_path)
                    if 'TIT2' in tags:
                        title = str(tags['TIT2'])
                    elif 'title' in audio.tags:
                        title = str(audio.tags['title'][0])

                    for tag_name in ['APIC:', 'APIC']:
                        if tag_name in tags:
                            apic = tags[tag_name]
                            if apic.mime.startswith('image/'):
                                album_art = Image.open(io.BytesIO(apic.data))
                                break
                except ID3NoHeaderError:
                    pass
            elif file_path.lower().endswith(".wav"):
                audio = WAVE(file_path)
                length = audio.info.length
                if 'title' in audio.tags:
                    title = str(audio.tags['title'][0])
            elif file_path.lower().endswith(".flac"):
                audio = FLAC(file_path)
                length = audio.info.length
                if 'title' in audio.tags:
                    title = str(audio.tags['title'][0])
                if audio.pictures:
                    for picture in audio.pictures:
                        if picture.mime.startswith('image/'):
                            album_art = Image.open(io.BytesIO(picture.data))
                            break

        except Exception as e:
            pass

        return length, album_art, title

    def load_default_album_art(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        default_art_path = os.path.join(base_path, "default_album_art.png")
        
        try:
            if os.path.exists(default_art_path):
                img = Image.open(default_art_path)
                self.display_album_art(img)
            else:
                self.album_art_canvas.delete("all")
                self.album_art_canvas.create_rectangle(0, 0, 400, 400, fill="black", outline="black")
        except Exception as e:
            self.show_error_message(_(f"Error loading default album art: {e}"))
            self.album_art_canvas.delete("all")
            self.album_art_canvas.create_rectangle(0, 0, 400, 400, fill="black", outline="black")


    def display_album_art(self, img):
        if img:
            canvas_width = self.album_art_canvas.winfo_width() if self.album_art_canvas.winfo_width() > 0 else 300
            canvas_height = self.album_art_canvas.winfo_height() if self.album_art_canvas.winfo_height() > 0 else 300
            
            img_width, img_height = img.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.album_photo = ImageTk.PhotoImage(resized_img)
            
            self.album_art_canvas.delete("all")
            self.album_art_canvas.create_image(canvas_width/2, canvas_height/2, image=self.album_photo, anchor="center")
        else:
            self.load_default_album_art()
            
    def play_selected_song(self, event=None):
        selected_indices = self.playlist_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            self.play_song(index)
        else:
            self.show_error_message(_("No song selected for playback."))

    def play_song(self, index):
        if 0 <= index < len(self.playlist):
            self.current_song_index = index
            song_path, length, album_art, title = self.playlist[index]

            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.paused = False
            self.song_title_label.config(text=title)
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(index)
            self.playlist_listbox.see(index)
            
            self.progress_bar.config(maximum=length)
            self.progress_var.set(0) # Dalváltáskor nullázzuk a progress bart
            
            self.display_album_art(album_art)

            self.play_pause_button.config(text="⏸️")

    def toggle_play_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            self.play_pause_button.config(text="⏸️")
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True
            self.play_pause_button.config(text="▶️")
        elif self.playlist and self.current_song_index != -1:
            self.play_song(self.current_song_index)
            self.play_pause_button.config(text="⏸️")
        elif self.playlist:
            self.play_song(0)
            self.play_pause_button.config(text="⏸️")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.play_pause_button.config(text="▶️")
        self.time_label.config(text="0:00 / 0:00")
        self.progress_var.set(0) # Progress var nullázása
        self.paused = False
        self.current_song_index = -1
        self.song_title_label.config(text=_("No song playing"))
        self.load_default_album_art()

    def play_next(self):
        if not self.playlist:
            return
        next_index = (self.current_song_index + 1) % len(self.playlist)
        self.play_song(next_index)

    def play_previous(self):
        if not self.playlist:
            return
        prev_index = (self.current_song_index - 1 + len(self.playlist)) % len(self.playlist)
        self.play_song(prev_index)

    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            self.repeat_button.config(text="🔂")
        else:
            self.repeat_button.config(text="🔁")

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def update_time(self):
        if pygame.mixer.music.get_busy() and not self.paused:
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            
            if self.current_song_index != -1:
                total_length = self.playlist[self.current_song_index][1]
                
                if current_pos >= total_length and total_length > 0:
                    if self.repeat_mode:
                        self.play_song(self.current_song_index)
                    else:
                        self.play_next()
                    
                    if not self.playlist and not self.repeat_mode:
                        self.stop_song()
                        
                else:
                    self.progress_var.set(current_pos) # Progress var frissítése
                    mins, secs = divmod(int(current_pos), 60)
                    total_mins, total_secs = divmod(int(total_length), 60)
                    self.time_label.config(text=f"{mins:02d}:{secs:02d} / {total_mins:02d}:{total_secs:02d}")
            else:
                self.progress_var.set(0) # Progress var nullázása
                self.time_label.config(text="0:00 / 0:00")
        elif not pygame.mixer.music.get_busy() and self.current_song_index != -1:
            if not self.paused and not self.repeat_mode:
                self.play_next()
            elif not self.paused and self.repeat_mode:
                self.play_song(self.current_song_index)
        
        self.master.after(1000, self.update_time)


    def seek_song(self, event):
        if self.current_song_index != -1:
            total_length = self.playlist[self.current_song_index][1]
            if total_length > 0:
                click_x = event.x
                bar_width = self.progress_bar.winfo_width()
                
                new_position = (click_x / bar_width) * total_length
                
                pygame.mixer.music.set_pos(new_position)
                self.progress_var.set(new_position) # Progress var beállítása
                
                if self.paused:
                    pygame.mixer.music.unpause()
                    self.paused = False
                    self.play_pause_button.config(text="⏸️")

    def filter_playlist(self, event=None):
        search_term = self.search_entry.get().lower()
        self.playlist_listbox.delete(0, tk.END)

        for i, (path, length, album_art, title) in enumerate(self.playlist):
            if search_term in title.lower():
                self.playlist_listbox.insert(tk.END, title)
                if i == self.current_song_index and pygame.mixer.music.get_busy():
                    self.playlist_listbox.selection_set(tk.END)
                    self.playlist_listbox.see(tk.END)

    def save_playlist(self):
        if not self.playlist:
            messagebox.showinfo(_("Save"), _("Playlist is empty. Nothing to save."))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".m3u",
            filetypes=[("M3U Playlist", "*.m3u"), (_("Text File"), "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for song_path, _, _, _ in self.playlist:
                        f.write(song_path + "\n")
                messagebox.showinfo(_("Save"), _("Playlist successfully saved!"))
            except Exception as e:
                self.show_error_message(_(f"Error saving playlist: {e}"))

    def load_playlist(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("M3U Playlist", "*.m3u"), (_("Text File"), "*.txt")]
        )
        if file_path:
            try:
                self.stop_song()
                self.playlist.clear()
                self.playlist_listbox.delete(0, tk.END)
                
                new_songs_added = False
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        song_path = line.strip()
                        if os.path.exists(song_path): 
                            length, album_art, title = self.get_file_metadata(song_path)
                            if length > 0 or song_path.lower().endswith((".mp3", ".wav", ".flac")):
                                self.playlist.append((song_path, length, album_art, title))
                                self.playlist_listbox.insert(tk.END, title)
                                new_songs_added = True
                            else:
                                self.show_error_message(_(f"Failed to load file from playlist: {os.path.basename(song_path)}"))
                        else:
                            self.show_error_message(_(f"File not found: {os.path.basename(song_path)}"))
                
                if new_songs_added and not pygame.mixer.music.get_busy() and self.current_song_index == -1:
                    self.play_song(0)
                    self.playlist_listbox.selection_set(0)
                    self.playlist_listbox.see(0)
                messagebox.showinfo(_("Load"), _("Playlist successfully loaded!"))
            except Exception as e:
                self.show_error_message(_(f"Error loading playlist: {e}"))

    def on_closing(self):
        self.is_closing = True
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.master.destroy()


# Alkalmazás indítása
if __name__ == "__main__":
    root = tk.Tk()
    player = MediaCatPlayer(root)
    
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        icon_path = os.path.join(bundle_dir, "mediacat_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
            player.playlist_window.window.iconbitmap(icon_path)
            player.album_art_window.window.iconbitmap(icon_path)
            player.player_controls_window.window.iconbitmap(icon_path)
            player.settings_window.window.iconbitmap(icon_path)
    except Exception as e:
        print(_(f"Error setting window icon: {e}"))

    root.mainloop()