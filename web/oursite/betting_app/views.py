from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
<<<<<<< HEAD

=======
def betting(request):
    return HttpResponse("Betting")
def start_league(request):
    return render(request, 'start.html')
>>>>>>> f300db489764cbd81934a44cc30741dcb5fdf353
