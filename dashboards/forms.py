__author__ = 'sukharni'

from django import forms
from models import *

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label="Topic")
    message = forms.CharField(widget=forms.Textarea, max_length=200)
    email = forms.EmailField(required = False)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message

#to upload files
class UploadForm(forms.Form):
    #author = forms.CharField(max_length=100, label="Author")
    title = forms.CharField(max_length=200, label = "Dashboard title")
    status = forms.ChoiceField(choices=(('1', 'Green',), ('2', 'Yellow',), ('3','Red')))
    type = forms.ChoiceField(choices=(('1', 'Curated',), ('2', 'Experimental',), ('3','Unfinished')))
    resource = forms.CharField(max_length=50, label = "Resource")
    file = forms.FileField(required=False)

class Login(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

#to register a new user
class Register(forms.Form):
    first = forms.CharField(max_length=20, required=True)
    last = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=40, required=False)
    login = forms.CharField(max_length=20, required=True)
    login_r = forms.CharField(max_length=20, required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password_r = forms.CharField(max_length=20, widget=forms.PasswordInput)

#to download files from the server
class Download(forms.Form):
    #overridden constructor that accepts key word argument called 'dash_name'
    def __init__(self,*args,**kwargs):
        dash_name = kwargs.pop("dash_name")
        #call super(base) class because code in super must be executed along with code in Download
        super(Download, self).__init__(*args,**kwargs)
        #to test whether all worked
        print "dash_name:", dash_name
        #print "unknown:", self.fields['select_all']   # self.fields - is a dictionary of all fields created
                                                       # when the class is called in the views
        #CHOICES = (('1', 'First',), ('2', 'Second',)) # an example of list of tuples for choices attribute
        self.fields['select_all'] = forms.ChoiceField(choices=dash_name) #I have to assign any values to widget
        # attributes in the constructor (i.e. choices=dash_name)

    search_by_name = forms.CharField(required=False)
    select_all = forms.ChoiceField(required=False) #this widget is created with already assigned choices, see above

#to delete a dashboard
class Delete(forms.Form):
    #overridden constructor that accepts key word argument called 'url_list'
    def __init__(self,*args,**kwargs):
        url_list = kwargs.pop("url_list")
        super(Delete, self).__init__(*args,**kwargs)
        #print "dash_name:", dash_name
        #print "unknown:", self.fields['select_all']   # self.fields - is a dictionary of all fields created
                                                       # when the class is called in the views
        #CHOICES = (('1', 'First',), ('2', 'Second',)) # an example of list of tuples for choices attribute
        self.fields['check_box'] = forms.ChoiceField(choices=url_list) #I have to assign any values to widget
        # attributes in the constructor (i.e. choices=dash_name)

    check_box = forms.ChoiceField()

#to unpublish a dashboard
class Unpublish(forms.Form):
    #overridden constructor that accepts key word argument called 'unpublished_list'
    def __init__(self, *args, **kwargs):
        unpublished_list = kwargs.pop("unpublished_list")
        super(Unpublish, self).__init__(*args, **kwargs)
        self.fields['check_box'] = forms.ChoiceField(choices = unpublished_list)

    check_box = forms.ChoiceField(required=False)