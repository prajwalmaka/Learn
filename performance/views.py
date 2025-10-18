from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DetailView
from django.db.models import Avg, Count
from assignments.models import Homework, Submission, Grade
from classes.models import ClassGroup

class PerformanceDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'performance/dashboard.html'

    def test_func(self):
        return self.request.user.is_teacher()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        classes = ClassGroup.objects.filter(teacher=self.request.user)
        context['classes'] = classes

        # Overall statistics
        assignments = Homework.objects.filter(created_by=self.request.user)
        submissions = Submission.objects.filter(homework__in=assignments)
        grades = Grade.objects.filter(submission__in=submissions)

        assignment_count = assignments.count()

        total_students = ClassGroup.objects.filter(teacher=self.request.user).aggregate(
            total=Count('students')
        )['total'] or 0

        total_possible_submissions = assignment_count * total_students

        context['total_assignments'] = assignment_count
        context['total_submissions'] = submissions.count()
        context['submission_rate'] = round(
            (submissions.count() / total_possible_submissions) * 100, 2
        ) if total_possible_submissions > 0 else 0
        context['avg_grade'] = grades.aggregate(avg=Avg('score'))['avg'] or 0

        return context


class ClassPerformanceView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = ClassGroup
    template_name = 'performance/class_performance.html'
    context_object_name = 'class'

    def test_func(self):
        return self.request.user.is_teacher() and self.get_object().teacher == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        students = self.object.students.all()
        assignments = Homework.objects.filter(class_group=self.object)
        assignment_count = assignments.count()

        student_data = []
        for student in students:
            submissions = Submission.objects.filter(
                homework__in=assignments,
                student=student
            )
            grades = Grade.objects.filter(submission__in=submissions)

            completed = submissions.filter(is_completed=True).count()
            avg_score = grades.aggregate(avg=Avg('score'))['avg'] or 0

            student_data.append({
                'student': student,
                'submissions': submissions.count(),
                'completion_rate': round((completed / assignment_count) * 100, 2) if assignment_count > 0 else 0,
                'avg_grade': avg_score,
            })

        # Optional: sort students by avg grade descending
        student_data.sort(key=lambda x: x['avg_grade'], reverse=True)

        context['student_data'] = student_data
        context['assignments'] = assignments
        return context
