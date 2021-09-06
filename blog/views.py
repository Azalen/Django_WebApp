from django.shortcuts import render

# List of Dictionaries
posts = [
    {
        'author': 'ArandSe',
        'title': 'Blog Post I',
        'content': 'Content I',
        'date_posted': 'August 27, 2021'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post II',
        'content': 'Content II',
        'date_posted': 'August 28, 2021'
    }
]

def home(request):
    # Dictionary to pass into render function
    context = {
        'posts': posts
    }

    # returns HTTP response in the background containing the code from the template file
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

# Create your views here.
