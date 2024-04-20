from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


from allauth.account.forms import SignupForm 

class CustomSignupForm(SignupForm):
    username = forms.CharField(label='Логин')
    email = forms.CharField(label='Эл. почта') 
    phone_number = forms.CharField(label='Номер телефона') 

    def save(self, request):
        if self.email:
            # Если email не пустой, проверяем на уникальность
            if user.objects.filter(email=self.email).exists():
                raise ValueError("Email must be unique.")
        user = super(CustomSignupForm, self).save(request)
        
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.is_patient = True
        
        user.save()
        return user
    

from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('pasport_id', 'phone' , 'adress', 'medcard', 'age') 