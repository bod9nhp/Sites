from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import Choice, Question,Article
from django.views import generic




def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.POST.get('plus'):
        selected_choice = question.choice_set.get(pk=request.POST['plus'])
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:details', args=(question.id,)))

    elif request.POST.get('minus'):
        selected_choice = question.choice_set.get(pk=request.POST['minus'])
        selected_choice.votes -= 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:details', args=(question.id,)))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_list = Choice.objects.filter(question_id=question_id)

    return render(request, 'detail.html', {'question': question, 'choice': choice_list})

def poll(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # if request.POST.get('plus'):
    #     selected_question = context.choice_set.get(pk=request.POST['plus'])
    #     selected_question.votes += 1
    #     selected_question.save()
    #     return HttpResponseRedirect(reverse('polls:index', args=(id.id,)))
    #
    # elif request.POST.get('minus'):
    #     selected_question = context.choice_set.get(pk=request.POST['plus'])
    #     selected_question.votes -= 1
    #     selected_question.save()
    #     return HttpResponseRedirect(reverse('polls:index', args=(id.id,)))
    return HttpResponse(template.render(context, request))



# def add_like(request):
#         article = get_object_or_404(Article)
#         article.likes += 1
#         article.save()
#
#
#
# def add_dislike(request):
#         article = get_object_or_404(Article)
#         article.dislikes += 1
#         article.save()
