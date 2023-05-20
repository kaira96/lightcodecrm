from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from account.models import MyUser
from .models import Topic, Question, Comment, AccessRights
from .forms import QuestionCreateForm, CommentCreateForm, AccessRightsForm


def index(request):
    main_topics = Topic.objects.filter(parent_topic__isnull=True)
    questions = Question.objects.all().order_by('-id')[:3]
    return render(request, template_name='forum/index.html', context={'main_topics': main_topics, 'questions': questions})


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 6), login_url='/registration/')
def user_ban(request):
    main_topics = Topic.objects.filter(parent_topic__isnull=True)

    current_user = MyUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        if current_user.status == 6 or current_user.is_admin == True:
            form = AccessRightsForm(data=request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.moderator = current_user
                obj.save()
                return redirect('banned_list')
            messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
        messages.error(request, 'Забанить может только Модератор или Админ')
    form = AccessRightsForm()
    return render(request, template_name='forum/cards.html', context={'main_topics': main_topics, 'form': form})


@method_decorator(login_required(login_url='/registration/'), name='dispatch')
class QuestionList(ListView):
    template_name = 'forum/list_questions.html'
    context_object_name = 'questions'
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_topics'] = Topic.objects.filter(parent_topic__isnull=True)

        return context

    def get_queryset(self):
        queryset = Question.objects.annotate(comment_count=Count('comment')).all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset


@login_required(login_url='/registration/')
def topic_detail_views(request, slug):
    main_topics = Topic.objects.filter(parent_topic__isnull=True)
    topic = Topic.objects.get(slug=slug)
    questions = Question.objects.annotate(comment_count=Count('comment')).filter(topic__slug=slug).order_by('-id')
    if request.method == 'POST':
        if request.user.is_banned == 1:
            form = QuestionCreateForm(data=request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = MyUser.objects.get(id=request.user.id)
                obj.topic = topic
                obj.save()
                return redirect('topic_detail', topic.slug)
            messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
        messages.error(request, 'К сожалению, ваш аккаунт был заблокирован из-за нарушения правил нашей платформы. Обратитесь к администрации, если у вас есть вопросы.')
    form = QuestionCreateForm()

    # задайте количество элементов на странице
    per_page = 15
    paginator = Paginator(questions, per_page)

    # получите номер страницы из GET-параметра
    page_number = request.GET.get('page')

    # получите объекты в соответствии с номером страницы
    page_obj = paginator.get_page(page_number)

    return render(request, template_name='forum/topic_detail.html', context={
        'main_topics': main_topics,
        'questions': page_obj,
        'topic': topic,
        'form': form})


@login_required(login_url='/registration/')
def question_detail_view(request, pk):
    main_topics = Topic.objects.filter(parent_topic__isnull=True)
    question = Question.objects.get(id=pk)
    comments = Comment.objects.filter(question=question)

    # Filter comments by created date
    order_by = request.GET.get('order_by')
    if order_by == 'asc':
        comments = comments.order_by('created_date')
    elif order_by == 'desc':
        comments = comments.order_by('-created_date')

    is_creator = Question.objects.filter(id=pk, user=request.user).exists()
    paginator = Paginator(comments, per_page=15)  # set number of comments per page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    if request.method == 'POST':
        if request.user.is_banned == 1:
            if 'comment_submit' in request.POST:
                comment_form = CommentCreateForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = request.user
                    comment.question = question
                    comment.save()
                    messages.success(request, 'Комментарий успешно добавлен.')
                    return redirect('question_detail', pk=pk)
                else:
                    messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате.')
            elif 'question_submit' in request.POST:
                question_form = QuestionCreateForm(request.POST, instance=question)
                if question_form.is_valid():
                    question_form.save()
                    messages.success(request, 'Вопрос успешно изменен.')
                    return redirect('question_detail', pk=pk)
                else:
                    messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате.')
        messages.error(request, 'К сожалению, ваш аккаунт был заблокирован из-за нарушения правил нашей платформы. Обратитесь к администрации, если у вас есть вопросы.')

    comment_form = CommentCreateForm()
    question_form = QuestionCreateForm(instance=question)

    return render(request, template_name='forum/question_detail.html', context={
        'main_topics': main_topics,
        'question': question,
        'comments': comments,
        'comment_form': comment_form,
        'question_form': question_form,
        'is_creator': is_creator,
    })


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 6), login_url='/registration/')
def banned_list_view(request):
    object_list = AccessRights.objects.all()
    main_topics = Topic.objects.filter(parent_topic__isnull=True)
    current_user = MyUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        if current_user.status == 6 or current_user.is_admin == True:
            form = AccessRightsForm(data=request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.moderator = current_user
                obj.save()
                return redirect('banned_list')
            messages.error(request, 'Повторите попытку, убедитесь что поля заполнены в правильном формате')
        messages.error(request, 'Забанить может только Модератор или Админ')
    form = AccessRightsForm()

    return render(request, template_name='forum/banned_list.html', context={
        'object_list': object_list,
        'main_topics': main_topics,
        'form': form,
    })


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 6), login_url='/registration/')
def user_delete(request, pk):
    user = AccessRights.objects.get(id=pk)
    user.delete()
    return HttpResponseRedirect(reverse('banned_list'))


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 6), login_url='/registration/')
def question_delete(request, pk):
    question = Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect(reverse('main_page'))


@user_passes_test(lambda u: u.is_authenticated and (u.is_admin or u.status == 6), login_url='/registration/')
def comment_delete(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return HttpResponseRedirect(reverse('main_page'))
















