# #views.py
# import threading
# #from .models import Crawl

# def startCrawl(request):
#     task = Crawl()
#     task.save()
#     t = threading.Thread(target=doCrawl,args=[task.id])
#     t.setDaemon(True)
#     t.start()
#     return JsonResponse({'id':task.id})

# def checkCrawl(request,id):
#     task = Crawl.objects.get(pk=id)
#     return JsonResponse({'is_done':task.is_done, result:task.result})

# def doCrawl(id):
#     task = Crawl.objects.get(pk=id)
#     # Do crawling, etc.

#     task.result = result
#     task.is_done = True
#     task.save()

import time
import threading

# We can literally cut this time by a magnitude of four if we run each process on its own thread
def paint_wall():
  print('Painting wall...')
  # Wait 30m
  time.sleep(5)
  print('Done painting wall')

walls_to_paint = 4

t = threading.Thread(target=paint_wall)
t.start()

print("main thread ready")