from django import forms

class SendingForm(forms.Form):
    """
    Form for sending email to admin
    """
    receiver = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    #TODO: prepopulate email field
    #TODO: send email

    def send_email(self):
        """
        Send email using the self.cleaned_data dictionary
        """
        print("sending email")
