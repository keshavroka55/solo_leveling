
from django import forms
from .models import Task, TaskCategory

class TaskForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=TaskCategory.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['category', 'name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            # Show only categories not yet used by this user
            used_categories = Task.objects.filter(user=user).values_list('category', flat=True)
            self.fields['category'].queryset = TaskCategory.objects.exclude(id__in=used_categories)



from django import forms
from .models import TaskProgress

class TaskProgressForm(forms.ModelForm):
    class Meta:
        model = TaskProgress
        fields = ['progress']

