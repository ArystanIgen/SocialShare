from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'bboard/index.html')

@login_required
def topics(request):

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    context = {'topics': topics}
    return render(request, 'bboard/topics.html', context)


@login_required
def topic(request,topic_id):
    "Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request,'bboard/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method!='POST':
        form = TopicForm()
        #Данные не отправились
    else:
        #Отправлены данные POST; обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('bboard:topics')
    #Вывести пустую или не действительную строку
    context={'form':form}
    return render(request,'bboard/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
    topic= Topic.objects.get(id=topic_id)
    if request.method!='POST':
        form = EntryForm()
        #Данные не отправились
    else:
        #Отправлены данные POST; обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('bboard:topic', topic_id=topic_id)
    #Вывести пустую или не действительную строку
    context={'topic':topic,'form':form}
    return render(request, 'bboard/new_entry.html', context)

@login_required
def edit_entry(request,entry_id):
    '''Редактирует существующую запись'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
    # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        #Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bboard:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'bboard/edit_entry.html', context)