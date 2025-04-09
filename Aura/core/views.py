from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .forms import UserRegisterForm, QuestionForm, AnswerForm
from .models import Question, Answer, Like


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all()
    form = AnswerForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)

    return render(request, 'question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })


@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)

    # Prevent users from liking their own answers
    if answer.author == request.user:
        return redirect('question_detail', pk=answer.question.id)

    # Avoid multiple likes from same user
    Like.objects.get_or_create(answer=answer, user=request.user)
    return redirect('question_detail', pk=answer.question.id)


@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user != question.author and not request.user.is_staff:
        return redirect('home')
    form = QuestionForm(request.POST or None, instance=question)
    if form.is_valid():
        form.save()
        return redirect('question_detail', pk=pk)
    return render(request, 'edit_question.html', {'form': form})


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user == question.author or request.user.is_staff:
        question.delete()
    return redirect('home')


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user != answer.author and not request.user.is_staff:
        return redirect('home')
    form = AnswerForm(request.POST or None, instance=answer)
    if form.is_valid():
        form.save()
        return redirect('question_detail', pk=answer.question.pk)
    return render(request, 'edit_answer.html', {'form': form})


@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user == answer.author or request.user.is_staff:
        answer.delete()
    return redirect('question_detail', pk=answer.question.pk)


def sorted_questions(request):
    sort_by = request.GET.get('sort', 'time')
    if sort_by == 'likes':
        questions = sorted(
            Question.objects.all(),
            key=lambda q: sum(a.likes.count() for a in q.answer_set.all()),
            reverse=True
        )
    else:
        questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'questions': questions})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'admin_panel.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_staff)
def toggle_admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = not user.is_staff
    user.save()
    return redirect('admin_panel')


@login_required
@user_passes_test(lambda u: u.is_staff)
def change_user_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = SetPasswordForm(user, request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('admin_panel')
    return render(request, 'change_password.html', {'form': form, 'target_user': user})


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = Question
    template_name = 'home.html'
    context_object_name = 'questions'

    def get_queryset(self):
        sort = self.request.GET.get('sort', 'time')
        queryset = Question.objects.all().annotate(
            total_likes=Count('answers__likes', distinct=True)
        )
        if sort == 'likes':
            return queryset.order_by('-total_likes')
        return queryset.order_by('-created_at')
