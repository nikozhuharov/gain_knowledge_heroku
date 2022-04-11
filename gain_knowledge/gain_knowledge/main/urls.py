from django.urls import path

from gain_knowledge.main.views import CategoryListView, CourseDetailView, display_question, final_score, \
    HomeView, CoursesListView, TestsListView, CreateCourseView, UserCoursesListView, CourseEditView, CourseDeleteView, \
    UserTestsListView, CreateTestView, EditTestView, DeleteTestView, UserQuestionsListView, CreateQuestionView, \
    DeleteQuestionView, EditQuestionView, QuestionDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='list categories'),
    path('categories/<int:pk>', CoursesListView.as_view(), name='list courses'),
    path('course/<int:pk>', CourseDetailView.as_view(), name='courses details'),
    path('tests/<int:pk>', TestsListView.as_view(), name='list tests'),
    path('question/<int:pk_test>/<int:count_questions>', display_question, name='display question'),
    path('final_score/<int:pk_test>', final_score, name='final score'),
    path('create_course/', CreateCourseView.as_view(), name='create course'),
    path('user_courses/', UserCoursesListView.as_view(), name='user list courses'),
    path('edit_course/<int:pk>', CourseEditView.as_view(), name='edit course'),
    path('delete_course/<int:pk>', CourseDeleteView.as_view(), name='delete course'),
    path('user_tests/<int:pk>', UserTestsListView.as_view(), name='user list tests'),
    path('create_test/<int:pk>', CreateTestView.as_view(), name='create test'),
    path('edit_test/<int:pk>', EditTestView.as_view(), name='edit test'),
    path('delete_test/<int:pk>', DeleteTestView.as_view(), name='delete test'),
    path('user_questions/<int:pk>', UserQuestionsListView.as_view(), name='user list questions'),
    path('create_question/<int:pk>', CreateQuestionView.as_view(), name='create question'),
    path('delete_question/<int:pk>', DeleteQuestionView.as_view(), name='delete question'),
    path('edit_question/<int:pk>', EditQuestionView.as_view(), name='edit question'),
    path('show_question/<int:pk>', QuestionDetailView.as_view(), name='show question'),
]