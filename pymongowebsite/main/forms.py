from django import forms


class CreateNewUser(forms.Form):


    username = forms.CharField(label="Username",max_length=200)

    name = forms.CharField(label="Full Name", max_length=200)


    age = forms.IntegerField(min_value=1,max_value=100)

    # (A,B) A is actual value, B is output
    # "choices" consists of list with multiple tuples

    gender = forms.ChoiceField(choices=[('girl',"Girl"),('boy',"Boy")])


    email = forms.EmailField()

