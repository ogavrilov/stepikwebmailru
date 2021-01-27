from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.views.decorators.http import require_GET
from qa.models import Question
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from qa.forms import AskForm
from qa.forms import AnswerForm
from qa.forms import SignUpForm
from qa.forms import LoginForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def question_object(request, *args, **kwargs):
    try:
        question_id = int(kwargs['question_id'])
    except:
        return HttpResponseBadRequest
    try:
        questionObject = Question.objects.get(id=question_id)
        answers = questionObject.answer_set.all()
    except ObjectDoesNotExist:
        raise Http404
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AnswerForm(request.user, request.POST, initial={'question': questionObject.id})
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(questionObject.get_url())
        else:
            form = AnswerForm(request.user, initial={'question': questionObject.id})
    else:
        form = None
    return render(request, 'question_object.html',
                  {'page_title': 'question view',
                   'question': questionObject,
                   'answers': answers,
                   'question_url': questionObject.get_url(),
                   'auth_user_authenticated': request.user.is_authenticated,
                   'auth_username': request.user.username,
                   'auth_logout_url': reverse('logout'),
                   'auth_current_url': questionObject.get_url(),
                   'auth_login_url': reverse('login'),
                   'auth_signup_url': reverse('signup'),
                   'form': form})

@require_GET
def question_list_popular(request, *args, **kwargs):
    try:
        question_list = Question.objects.popular()
    except:
        return HttpResponseServerError
    paginator, curr_page = __paginate__(request, question_list)
    paginator.baseurl = reverse('popular')
    return render(request, 'question_list.html', {
        'page_title': 'popular questions',
        'question_list': curr_page.object_list,
        'ask_url': reverse('ask'),
        'auth_user_authenticated': request.user.is_authenticated,
        'auth_username': request.user.username,
        'auth_logout_url': reverse('logout'),
        'auth_current_url': reverse('popular') + '?page=' + str(curr_page.number),
        'auth_login_url': reverse('login'),
        'auth_signup_url': reverse('signup'),
        'paginator': paginator, 'curr_page': curr_page
    })

@require_GET
def question_list_latest(request, *args, **kwargs):
    try:
        question_list = Question.objects.new()
    except:
        return HttpResponseServerError
    paginator, curr_page = __paginate__(request, question_list)
    paginator.baseurl = reverse('new')
    return render(request, 'question_list.html', {
        'page_title': 'popular questions',
        'question_list': curr_page.object_list,
        'ask_url': reverse('ask'),
        'auth_user_authenticated': request.user.is_authenticated,
        'auth_username': request.user.username,
        'auth_logout_url': reverse('logout'),
        'auth_current_url': reverse('new') + '?page=' + str(curr_page.number),
        'auth_login_url': reverse('login'),
        'auth_signup_url': reverse('signup'),
        'paginator': paginator, 'curr_page': curr_page
    })

def askform(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AskForm(request.user, request.POST)
            if form.is_valid():
                questionObject = form.save()
                return HttpResponseRedirect(questionObject.get_url())
        else:
            form = AskForm(request.user)
        return render(request, 'question_add.html', {
            'page_title': 'question add',
            'question_url': reverse('ask'),
            'auth_user_authenticated': request.user.is_authenticated,
            'auth_username': request.user.username,
            'auth_logout_url': reverse('logout'),
            'auth_current_url': reverse('new'),
            'auth_login_url': reverse('login'),
            'auth_signup_url': reverse('signup'),
            'form': form})
    else:
        return HttpResponseRedirect(reverse('signup'), {'redirectPage': reverse('ask')})

def signup(request, *args, **kwargs):
    # determ redirect page
    redirectPage = request.POST.get('redirectPage')
    if redirectPage is None or redirectPage == '':
        redirectPage = reverse('root')
    # forms
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirectPage)
    elif request.method == 'POST':
        form = SignUpForm(redirectPage, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'), {'redirectPage': redirectPage})
    else:
        form = SignUpForm(redirectPage)
    return render(request, 'registration/signup.html', {
        'page_title': 'sign up',
        'signup_url': reverse('signup'),
        'form': form})

def login(request, *args, **kwargs):
    # determ redirect page
    redirectPage = request.POST.get('redirectPage')
    if redirectPage is None or redirectPage == '':
        redirectPage = reverse('root')
    # forms
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirectPage)
    elif request.method == 'POST':
        form = LoginForm(redirectPage, request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(redirectPage)
    else:
        form = LoginForm(redirectPage)
    return render(request, 'registration/login.html', {
        'page_title': 'login',
        'login_url': reverse('login'),
        'signup_url': reverse('signup'),
        'form': form})

def logout(request, *args, **kwargs):
    # determ redirect page
    redirectPage = request.POST.get('redirectPage')
    if redirectPage is None or redirectPage == '':
        redirectPage = reverse('root')
    # forms
    if request.user.is_authenticated:
        auth_logout(request)
        return HttpResponseRedirect(redirectPage)
    else:
        return render(request, 'registration/logged_out.html', {
            'page_title': 'logout',
            'auth_user_authenticated': request.user.is_authenticated,
            'auth_username': request.user.username,
            'auth_logout_url': reverse('logout'),
            'auth_current_url': redirectPage,
            'auth_login_url': reverse('login'),
            'auth_signup_url': reverse('signup')
            })

def __paginate__(request, querySet):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(querySet, limit)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page