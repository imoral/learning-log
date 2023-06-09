from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect

from .forms import TopicForm, EntryForm
from .models import Topic, Entry


def check_owner(topic_: Topic, user: User):
    """Make sure the topic belongs to the current user"""
    if topic_.owner != user:
        raise Http404


# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
    """Show all topics."""
    topics_ = Topic.objects.order_by('date_added')
    context = {'topics': topics_, 'filter': False}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic_ = Topic.objects.get(id=topic_id)

    check_owner(topic_, request.user)

    entries = topic_.entry_set.order_by('-date_added')
    context = {'topic': topic_, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request: HttpRequest):
    """Save a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST dat submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            topic_: Topic = form.save(commit=False)
            topic_.owner = request.user
            form.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Save a new entry for a particular topic."""
    topic_ = Topic.objects.get(id=topic_id)

    check_owner(topic_, request.user)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST dat submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_: Entry = form.save(commit=False)
            new_entry_.topic = topic_
            new_entry_.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic_, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic_ = entry.topic

    check_owner(topic_, request.user)

    if request.method != 'POST':
        # Initial request, pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST dat submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_.id)

    # Display a blank or invalid form.
    context = {'entry': entry, 'topic': topic_, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def my_topics(request):
    """Show all topics by user."""
    topics_ = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics_, 'filter': True}
    return render(request, 'learning_logs/topics.html', context)
