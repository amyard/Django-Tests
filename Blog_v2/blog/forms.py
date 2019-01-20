from django import forms
from .models import Tag, Comments
from django.core.exceptions import ValidationError

class TagForm(forms.ModelForm):

	class Meta:
		model = Tag
		fields = ['title', 'slug']

		widgets = {
			'title': forms.TextInput(attrs = {'class':'form-control'}),
			'slug': forms.TextInput(attrs = {'class':'form-control'}),
		}

	# make slug lowercase
	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()  # self.cleaned_data.get['slug']

		if new_slug == 'create':
			raise ValidationError('Slug may not be "Create"')

		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError('Slug must be unique. Slug already exists.')

		return new_slug


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ['content']

		widgets = {'content': forms.Textarea(attrs = {'class':'form-control', 'rows': 5, 'cols':150})}