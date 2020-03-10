from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "no seleccionaste una opción",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def crearForm(request):
    return render(request, 'polls/create.html')


def save(request):
    try:
        question = Question(question_text=request.POST['pregunta'])
        question.save()
        return render(request, 'polls/detail.html', {
            'question': question,
            'mensaje': "se ha creado la pregutna correctamente",
        })
    except:
        return render(request, 'polls/create.html', {
            'error_message': "no se ha podido crear la pregunta"
        })


def choiceForm(request, newcontext={}):
    preguntas = Question.objects.all()
    context = {'preguntas': preguntas, }
    context.update(newcontext)
    return render(request, 'polls/create-choice.html', context)


def saveChoice(request):
    question = get_object_or_404(Question, pk=request.POST['question'])
    try:
        question.choice_set.create(
            choice_text=request.POST['respuesta'], votes=0)
    except:
        context = {
            'message': 'no se ha podido crear la respuesta',
            'message_class': 'alert alert-success',
        }
        return choiceForm(request, context)
        
    else:
        context = {
            'message': ' se ha creado la respuesta exitosamente',
            'message_class': 'alert alert-success',
        }
        return choiceForm(request, context)
