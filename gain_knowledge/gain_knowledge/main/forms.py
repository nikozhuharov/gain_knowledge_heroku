from django import forms

from gain_knowledge.common.helper import BootstrapFormMixin
from gain_knowledge.main.models import Question, Course, Test


class CreateCourseForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        course = super().save(commit=False)

        course.user = self.user
        if commit:
            course.save()

        return course

    class Meta:
        model = Course
        fields = ('title', 'description', 'picture', 'video', 'document', 'category')


class CreateTestForm(BootstrapFormMixin, forms.ModelForm):

    def __init__(self, course_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id = course_id
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        test = super().save(commit=False)

        test.course_id = self.course_id

        if commit:
            test.save()

        return test

    class Meta:
        model = Test
        fields = ('title',)


class CreateQuestionForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, test_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_id = test_id
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        question = super().save(commit=False)

        question.test_id = self.test_id

        if commit:
            question.save()

        return question

    class Meta:
        model = Question
        fields = ('title', 'first_option', 'second_option', 'third_option', 'fourth_option', 'correct_answer')
        widgets = {
            'title': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Describe Question',
                }
            ),
            'first_option': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Insert A Choice',
                }
            ),
            'second_option': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Insert B Choice',
                }
            ),
            'third_option': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Insert C Choice',
                }
            ),
            'fourth_option': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Insert D Choice',
                }
            ),
        }


class CourseEditForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Course
        fields = ('title', 'description', 'picture', 'video', 'document', 'category')


class EditTestForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Test
        fields = ('title',)


class EditQuestionForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Question
        fields = ('title', 'first_option', 'second_option', 'third_option', 'fourth_option', 'correct_answer')
        widgets = {
            'title': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'first_option': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'second_option': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'third_option': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'fourth_option': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
        }