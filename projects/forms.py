from django.forms import ModelForm
from projects import models
from django import forms

class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'title',
            'description',
            'featured_image',
            'live_demo_link',
            'source_code_link',
            'tags'
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
            })


class ReviewForm(ModelForm):
    class Meta:
        model = models.Review
        fields = [
            'value',
            'body',
        ]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({
                'class':'input',
            })
