from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from . import util
import logging
from colorama import init, Fore, Back, Style

logging.basicConfig(format=f'%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
init(autoreset=True)


# Create your views here.
def list_all_mangas(request):
    manga_list = []
    for k,v in util.ALL_MANGAS.items():
        manga_dict = {
            'mangaName' : k,
            'latestChapter' : v,
            'thumb' :  'http://' + request.get_host() + f"/{k}" + f"/thumb"
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
        file = util.doesChapterFileExists(util.getMangaOriginalName(manga_name_filtered), chapter, image_file)
        if manga_filtered == manga_name_filtered and int(chapter) <= util.ALL_MANGAS[manga] and file:
            return HttpResponse(file, content_type=f"image/{image_file[-3:]}")


    return HttpResponseNotFound()


def get_manga_thumb(request, manga_name):
    manga_name_filtered = ''.join(e for e in manga_name if e.isalnum()).lower()
    for manga in util.ALL_MANGAS.keys():
        manga_filtered = ''.join(e for e in manga if e.isalnum()).lower()
        if manga_filtered == manga_name_filtered:
            file = util.doesThumbFileExists(util.getMangaOriginalName(manga_name_filtered))
            if file:
                return HttpResponse(file, content_type=f"image/jpg")
            
    return HttpResponseNotFound()
        
    
            
    