from urllib.error import HTTPError
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import requests
from . import util
import logging
from colorama import init, Fore, Back, Style
import base64

logging.basicConfig(format=f'%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
init(autoreset=True)


# Create your views here.
def list_all_mangas(request):
    manga_list = []
    for k,v in util.ALL_MANGAS.items():
        manga_dict = {
            'mangaName' : k,
            'latestChapter' : v
        }
        manga_list.append(manga_dict)
    return JsonResponse(manga_list, safe=False)

def get_manga_chapter(request, manga_name, chapter):
    
    # Checking for valid manga name and chapter
    # applying filter to remove special chars and spaces  
    manga_name_filtered = ''.join(e for e in manga_name if e.isalnum()).lower()
    for manga in util.ALL_MANGAS.keys():
        manga_filtered = ''.join(e for e in manga if e.isalnum()).lower()
        if manga_filtered == manga_name_filtered and int(chapter) <= util.ALL_MANGAS[manga]:
            return JsonResponse(util.get_manga_chapter(manga_name, chapter, request.get_host()), safe=False, json_dumps_params={'indent': 2})

    return HttpResponseNotFound()


def get_manga_images(request, manga_name, chapter, image_file):
    
    # Checking for valid manga name, chapter and file
    # applying filter to remove special chars and spaces
    manga_name_filtered = ''.join(e for e in manga_name if e.isalnum()).lower()
    for manga in util.ALL_MANGAS.keys():
        manga_filtered = ''.join(e for e in manga if e.isalnum()).lower()
        file = util.doesFileExists(util.getMangaOriginalName(manga_name), chapter, image_file)
        if manga_filtered == manga_name_filtered and int(chapter) <= util.ALL_MANGAS[manga] and file:
            return HttpResponse(file, content_type=f"image/{image_file[-3:]}")


    return HttpResponseNotFound()
            
        
    
            
    