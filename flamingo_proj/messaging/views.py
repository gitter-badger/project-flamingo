from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
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
def outbox(request):
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
        form.recipient = MyUser.objects.get(id=request.POST["recipient"])
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
