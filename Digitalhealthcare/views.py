from django.shortcuts import render
from doctors.models import Post

def home(request):

    posts = Post.objects.all().order_by('-published_date')
    context = {'posts': posts}

    return render(request, 'home.html', context)