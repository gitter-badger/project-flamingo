from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Message
from .forms import MessageForm
from profiles.models import MyUser


@login_required
def inbox(request):
    message_list = Message.objects.inbox_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'messaging/inbox.html', context=context)


@login_required
def sent(request):
    message_list = Message.objects.outbox_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'messaging/outbox.html', context=context)


@login_required
def trash(request):
    message_list = Message.objects.trash_for(request.user)
    context = {'message_list': message_list}
    return render(request, 'messaging/trash.html', context=context)


@login_required
def compose(request):
    if request.method == "POST":
        form = MessageForm(request.POST or None)
        print request.POST
        form.message_body = request.POST["message_body"]
        form.recipient = request.POST["recipient"]
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "You messaged successfully!")
            return JsonResponse({'you_sent': message.message_body,
                                 'messageId': message.id})
        else:
            print form.errors
    else:
        messages.error(request, "Something went wrong with this message!")
        return JsonResponse({'message_body': 'Error!'})

def detail(request, message_id):
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404
    if message.read_at is None and message.recipient == user:
        message.read_at = now
        message.save()

    context = {'message': message}
    return render(request, "message.html", context=context)


def delete_message(request, message_id):
    now = timezone.now()
    deleted_message = get_object_or_404(Message, id=message_id)
    deleted = False
    if deleted_message.sender == request.user:
        if deleted_message.sender_deleted_at is None:
            deleted_message.sender_deleted_at = now
            deleted = True
        else:
            deleted_message.add_permanent_delete()
    if deleted_message.recipient == request.user:
        if deleted_message.recipient_deleted_at is None:
            deleted_message.recipient_deleted_at = now
            deleted = True
        else:
            deleted_message.add_permanent_delete()
    if deleted:
        deleted_message.save()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages:inbox')
    elif deleted_message.deleted():
        deleted_message.delete()
        return redirect('messages:trash')
    else:
        raise Http404("You cannot delete this message!")

