from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from vehicles.forms import MessagesForm
from vehicles.models import Vehicle


def send_message_view(request, vehicle_id):
    message_form = MessagesForm(request.POST)
    if message_form.is_valid():
        admin = User.objects.get(username='admin')
        vehicle = Vehicle.objects.get(id=vehicle_id)
        new_message = message_form.save(commit=False)
        new_message.sender = request.user
        new_message.receiver = admin
        new_message.vehicle = vehicle
        new_message.save()
    else:
        messages.error(request, 'Error sending message')
    return redirect('reservation:reserve', vehicle_id)
