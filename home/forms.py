from django import forms
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from .models import Item, AuthorItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'year', 'area', 'repository', 'content_type', 'pdf']

    def clean(self):
        cleaned_data = super().clean()
        pdf = cleaned_data.get('pdf')

        if not pdf:
            raise forms.ValidationError("Porfavor suba un archivo pdf.")

        if pdf and not pdf.name.endswith('.pdf'):
            raise forms.ValidationError("Solo se admiten archivos pdf.")

        return cleaned_data
    
class AuthorItemForm(forms.ModelForm):
    first_name = forms.CharField(max_length=124, required=True)
    last_name = forms.CharField(max_length=124, required=True)

    class Meta:
        model = AuthorItem
        fields = ['first_name', 'last_name']

class BaseAuthorItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        has_author = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                has_author = True
                break

        if not has_author:
            raise forms.ValidationError("Debe agregar al menos un autor.")

AuthorItemFormSet = inlineformset_factory(
    Item, AuthorItem, form=AuthorItemForm, formset=BaseAuthorItemFormSet, extra=2, can_delete=True
)