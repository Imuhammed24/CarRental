from django.shortcuts import render


def index_view(request):
    context = {
        'html_title': 'WELCOME TO CARTAL',
    }
    return render(request, 'index.html', context)
