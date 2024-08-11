from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')


def events(request):
    pass


def create_event(request):
    pass
