from django import forms
from django.contrib.auth import mixins as auth_mixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import ListView, DetailView

from gain_knowledge.accounts.models import CurrentResult
from gain_knowledge.common.helper import BootstrapFormMixin, BootstrapRadioFormMixin
from gain_knowledge.common.view_mixins import RedirectToCategories
from gain_knowledge.main.forms import CreateCourseForm, CreateTestForm, CreateQuestionForm, CourseEditForm, \
    EditTestForm, EditQuestionForm
from gain_knowledge.main.models import Category, Course, Test, Question




class HomeView(RedirectToCategories, views.TemplateView):
    template_name = 'main/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'main/list_categories.html'
    context_object_name = 'categories_list'


class CoursesListView(ListView):
    model = Course
    template_name = 'main/list_courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        category = get_object_or_404(Category, id=self.kwargs['pk'])
        return Course.objects.filter(category=category)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'main/course_details.html'
    context_object_name = 'course_detail'


class TestsListView(ListView):
    model = Test
    template_name = 'main/list_tests.html'
    context_object_name = 'tests_list'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['pk'])
        return Test.objects.filter(course_id=course.id)


def display_question(request, pk_test, count_questions):

    question_objects = Question.objects.filter(test_id=pk_test)

    if question_objects:

        question = question_objects[count_questions]

        options = [("A", question.first_option),
                   ("B", question.second_option),
                   ("C", question.third_option),
                   ("D", question.fourth_option)]

        class QuestionForm(forms.Form):

            answer = forms.CharField(label=question.title,
                                     widget=forms.RadioSelect(choices=options)
                                     )

        if request.method == 'POST':
            form = QuestionForm(request.POST)
            current_result = CurrentResult.objects.get(user_id=request.user.id)
            if form.is_valid():
                if form.cleaned_data['answer'] == question.correct_answer:
                    current_result.correct_answers += 1
                else:
                    current_result.incorrect_answers += 1
                current_result.save()

                if count_questions < len([x for x in Question.objects.filter(test_id=pk_test)])-1:
                    count_questions += 1
                    return redirect('display question', pk_test=pk_test, count_questions=count_questions)
                else:
                    return redirect('final score', pk_test=pk_test)
        else:
            form = QuestionForm()

        context = {
            'form': form,
            'question': question,
            'pk_test': pk_test,
            'count_questions': count_questions
        }

        return render(request, 'main/display_question.html', context)
    else:
        context = {
            'pk_test': pk_test,
            'count_questions': count_questions,
            'no_question': True,
        }

        return render(request, 'main/display_question.html', context)


def final_score(request, pk_test):
    current_result = CurrentResult.objects.get(user_id=request.user.id)
    total_answers = current_result.correct_answers + current_result.incorrect_answers
    correct_answers = current_result.correct_answers
    incorrect_answers = current_result.incorrect_answers
    percentage = int(correct_answers/total_answers*100)
    context = {
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_answers': total_answers,
        'percentage': percentage,
        'pk_test': pk_test
    }
    current_result.correct_answers = 0
    current_result.incorrect_answers = 0
    current_result.save()

    return render(request, 'main/final_score.html', context)


class CreateCourseView(auth_mixin.LoginRequiredMixin, views.CreateView):
    template_name = 'main/course_create.html'
    form_class = CreateCourseForm
    success_url = reverse_lazy('list categories')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class UserCoursesListView(ListView):
    model = Course
    template_name = 'main/list_user_courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        user = self.request.user.id
        return Course.objects.filter(user_id=user)


class CourseEditView(views.UpdateView):
    model = Course
    template_name = 'main/course_edit.html'
    form_class = CourseEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('user list courses')


class CourseDeleteView(views.DeleteView):
    model = Course
    template_name = 'main/course_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })
        return context

    def get_success_url(self):
        return reverse_lazy('user list courses')


class UserTestsListView(ListView):
    model = Test
    template_name = 'main/list_user_tests.html'
    context_object_name = 'tests_list'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['pk'])
        return Test.objects.filter(course_id=course.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs['pk'])
        context['course'] = course
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class CreateTestView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateTestForm
    template_name = 'main/test_create.html'

    def get_success_url(self):
        course = self.get_context_data()['course']
        course_id = course.id
        return reverse_lazy('user list tests', kwargs={'pk': course_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['course_id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs['pk'])
        context['course'] = course
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class EditTestView(views.UpdateView):
    model = Test
    template_name = 'main/test_edit.html'
    form_class = EditTestForm

    def get_success_url(self):
        test = self.get_context_data()['test']
        return reverse_lazy('user list tests', kwargs={'pk': test.course_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, id=self.kwargs['pk'])
        course_id = test.course_id
        course = Course.objects.get(pk=course_id)
        context['test'] = test
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class DeleteTestView(views.DeleteView):
    model = Test
    template_name = 'main/test_delete.html'

    def get_success_url(self):
        test = self.get_context_data()['test']
        return reverse_lazy('user list tests', kwargs={'pk': test.course_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, id=self.kwargs['pk'])
        course_id = test.course_id
        course = Course.objects.get(pk=course_id)
        context['test'] = test
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class UserQuestionsListView(ListView):
    model = Question
    template_name = 'main/list_user_questions.html'
    context_object_name = 'questions_list'

    def get_queryset(self):
        test = get_object_or_404(Test, id=self.kwargs['pk'])
        return Question.objects.filter(test_id=test.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, id=self.kwargs['pk'])
        course_id = test.course_id
        course = Course.objects.get(pk=course_id)
        context['test'] = test
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class CreateQuestionView(auth_mixin.LoginRequiredMixin, views.CreateView):
    form_class = CreateQuestionForm
    template_name = 'main/question_create.html'

    def get_success_url(self):
        test = self.get_context_data()['test']
        test_id = test.id
        return reverse_lazy('user list questions', kwargs={'pk': test_id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['test_id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test = get_object_or_404(Test, id=self.kwargs['pk'])
        course_id = test.course_id
        course = Course.objects.get(pk=course_id)
        context['test'] = test
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class DeleteQuestionView(views.DeleteView):
    model = Question
    template_name = 'main/question_delete.html'

    def get_success_url(self):
        question = self.get_context_data()['question']
        test_id = question.test_id
        return reverse_lazy('user list questions', kwargs={'pk': test_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['pk'])
        test = Test.objects.get(pk=question.test_id)
        course = Course.objects.get(pk=test.course_id)
        context['question'] = question
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class EditQuestionView(views.UpdateView):
    model = Question
    template_name = 'main/question_edit.html'
    form_class = EditQuestionForm

    def get_success_url(self):
        question = self.get_context_data()['question']
        test_id = question.test_id
        return reverse_lazy('user list questions', kwargs={'pk': test_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['pk'])
        test = Test.objects.get(pk=question.test_id)
        course = Course.objects.get(pk=test.course_id)
        context['question'] = question
        context['is_owner'] = course.user_id == self.request.user.id
        return context


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'main/question_details.html'
    context_object_name = 'question_detail'


