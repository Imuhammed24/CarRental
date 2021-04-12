from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import SearchQuery
from vehicles.models import Vehicle


@login_required(login_url='/')
def search_view(request):
    query = request.GET.get('q', None)

    if query is not None:
        vehicles = Vehicle.objects.all()
        SearchQuery.objects.create(user=request.user, query=query)
        search_result = Vehicle.objects.search(query=query)
        context = {'query': query,
                   'vehicles': vehicles,
                   'search_result': search_result}

        return render(request, 'searches/view.html', context)
    else:
        return redirect('account:home')

