from django.shortcuts import render

def home(request):
    # returns HTTP response in the background containing the code from the template file
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

# Create your views here.
