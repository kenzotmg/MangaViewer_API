from enum import auto
import os
from colorama import init, Style, Fore
import logging
import re
import environ
import os

init(autoreset=True)
logging.basicConfig(format=f'%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

env = environ.Env()

# CONSTANTS
MANGA_DIR = env('MANGA_DIR')
MANGA_THUMB_DIR = env('MANGA_THUMB_DIR')

# Returns a dictionary where KEY = Manga Name and VALUE = Latest Chapter
def get_mangas():
    mangas = {}
    # Get Manga Names and Latest Chapter
    for manga in os.listdir(MANGA_DIR):
        last_chapter = 0
        for chapter in os.listdir(os.path.join(MANGA_DIR, manga)):
            try:
                if int(last_chapter) < int(chapter):
                    last_chapter = int(chapter)
            except ValueError:
                logging.error(f'{Fore.RED}Manga {manga} has invalid chapter folder: {chapter}{Style.RESET_ALL}')

        mangas[manga] = last_chapter
        
    return mangas

    
def get_manga_chapter(manga_name, chapter, host):
    for manga in os.listdir(MANGA_DIR):
        if filter_str(manga) == manga_name:
            manga_name = manga
            
    base_url = 'http://' + host + f"/{manga_name}" + f"/{chapter:02d}"
    path = MANGA_DIR + f'\{manga_name}' + f'\{chapter:02d}'
    
    images_url = []
    chapterImagesFiles = os.listdir(path)
    chapterImagesFiles.sort(key=natural_keys)
    for file in chapterImagesFiles:
        chapterDict = {
            'imageUrl' : f'{base_url}' + f'/{file}'
        }
        images_url.append(chapterDict)
        
    return images_url

# Filter out any special character and spaces in string
def filter_str(text):
    return ''.join(e for e in text if e.isalnum()).lower()


def doesChapterFileExists(manga_name, chapter, file):
    path = MANGA_DIR + f"\{manga_name}" + f"\{chapter:02d}" + f"\{file}"
    if os.path.exists(path):
        with open(path, 'rb') as image_file:
            file_binary = image_file.read()
        return file_binary
    
    else:
        return False
            
def doesThumbFileExists(manga_name):
    path = MANGA_THUMB_DIR + f"\{manga_name}" + fr"/thumb.jpg"
    if os.path.exists(path):
        with open(path, 'rb') as image_file:
            file_binary = image_file.read()
        return file_binary
    
    return False
            
def getMangaOriginalName(manga_name):
    for manga in os.listdir(MANGA_DIR):
        if filter_str(manga) == filter_str(manga_name):
            return manga
    

# Functions to sort alphabetically files with number in their names
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

  
    
ALL_MANGAS = get_mangas()