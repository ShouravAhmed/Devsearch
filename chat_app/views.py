from django.shortcuts import render, redirect
from django.contrib import messages

from .utils import get_text_messages, inbox_preview
from .models import text_message

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def chatapp(request, pk):

    if str(request.user.profile.id) == str(pk):
        messages.error(request, "You can't chat with yourself")
        return redirect('profiles')

    text_messages, receiver = get_text_messages(request, pk)
    
    if request.method == 'POST':
        message = request.POST['message']
        msg = text_message.objects.create(
            body = message,
            sender = request.user.profile,
            receiver = receiver
        )
        msg.save()
        text_messages, receiver = get_text_messages(request, pk)

    context = {'text_messages':text_messages, 'receiver':receiver}    
    
    return render(request, 'chat_app/chatapp.html', context)

@login_required(login_url='login')
def inbox(request):
    msg_list, new_msg = inbox_preview(request)
    context = {
        'msg_list':msg_list,
        'new_msg':new_msg,
    }
    return render(request, 'chat_app/inbox.html', context)

