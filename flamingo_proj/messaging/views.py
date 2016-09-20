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
            messages.error(request, "You entered something wrong here!")
            return JsonResponse({'message_body': 'Error!'})

    else:
        messages.error(request, "Something went wrong with this message!")
        return JsonResponse({'message_body': 'Error!'})

def detail(request, message_id):
    user = request.user
    now = timezone.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.recipient != user):
        raise Http404

    context = {'message': message}
    return render(request, "message.html", context=context)


def delete_message(request, message_id):
    now = timezone.now()
    deleted_message = get_object_or_404(Message, id=message_id)
    deleted = False
    if deleted_message.sender == request.user:
        deleted = True
        if deleted_message.sender_deleted_at is None:
            deleted_message.sender_deleted_at = now
        else:
            deleted_message.sender_deleted_perm = True
    if deleted_message.recipient == request.user:
        deleted = True
        if deleted_message.recipient_deleted_at is None:
            deleted_message.recipient_deleted_at = now
        else:
            deleted_message.recipient_deleted_perm = True
    if deleted_message.for_delete():
        deleted_message.delete()
        return redirect('messages:trash')
    elif deleted:
        deleted_message.save()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages:inbox')
    else:
        raise Http404("You cannot delete this message!")

