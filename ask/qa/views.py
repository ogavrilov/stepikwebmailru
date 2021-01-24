from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.views.decorators.http import require_GET
from qa.models import Question
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

def test(request, *args, **kwargs):
    return HttpResponse('OK')

@require_GET
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
    return render(request, 'question_object.html', {'page_title': 'question view', 'question': questionObject, 'answers': answers})

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
        'paginator': paginator, 'curr_page': curr_page
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
    #print('------------get params:')
    #for get_key, get_value in request.GET.items():
    #    print('------------' + str(get_key) + '|' + str(get_value) + '|')
    paginator = Paginator(querySet, limit)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page