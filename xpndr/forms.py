from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user','date','time','satellite', 'transponder', 'frequency','user_detail','complaint_type','impact',
        'issue_time','ticket','helix_dc','operating_point','bandwidth','priority','details','photo','upload','active']
        widgets={
            'user':forms.HiddenInput(), 
            'date':forms.DateInput(attrs={'type':'date','class':'form-control w-50'}),
            # 'date':forms.DateInput(attrs={'type':'date','class':'form-control w-50'}, format='%d %B %Y'),
            # 'date':forms.DateInput(attrs={'type':'date-local','class':'form-control', 'placeholder':'Select a date'}, format='%d %b %Y'),
            'time':forms.TimeInput(attrs={'type':'time','class':'form-control w-50'}),
            # 'time':forms.TimeInput(attrs={'type':'time','class':'form-control w-50'},format='%H %M'),
            'satellite':forms.Select(attrs={'class':'form-select '}),
            'transponder':forms.Select(attrs={'class':'form-select'}),
            'frequency':forms.TextInput(attrs={'class':'form-control'}),
            'user_detail':forms.TextInput(attrs={'class':'form-control'}),
            'complaint_type':forms.Select(attrs={'class':'form-select'}),
            'impact':forms.TextInput(attrs={'class':'form-control'}),
            'issue_time': forms.DateTimeInput(attrs={'type':'datetime-local','class':'form-control w-50'}, format='%Y-%m-%dT%H:%M'),
            # 'issue_time':forms.DateTimeInput(attrs={'class':'form-control'}),
            'ticket':forms.HiddenInput(attrs={'class':'form-control'}),
            'helix_dc':forms.TextInput(attrs={'class':'form-control'}),
            'operating_point':forms.Select(attrs={'class':'form-select '}),
            'bandwidth':forms.TextInput(attrs={'class':'form-control'}),
            'priority':forms.Select(attrs={'class':'form-select'}),
            'details':forms.Textarea(attrs={'class':'form-control'}),           
            # 'upload':forms.FileInput(attrs={'class':'input-group form-control'}),
            # 'photo':forms.FileInput(attrs={'class':'form-control'}),
            'active':forms.CheckboxInput(attrs={ 'id':"flexCheckDefault"}),
            # 'active':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':"flexCheckDefault"}),
        }

# class SatDetailForm(forms.ModelForm):
    
#     class Meta:
#         model = Comment
#         fields = ['satellite']
