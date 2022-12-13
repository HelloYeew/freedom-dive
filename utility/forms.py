from django import forms

from users.models import SignUpRequest


class ImportSpecificBeatmapSetForm(forms.Form):
    beatmapset_id = forms.IntegerField(label='Beatmapset ID', help_text='The ID of the beatmapset you want to import.')

    class Meta:
        fields = ['beatmapset']


class CreateSignUpRequestForm(forms.ModelForm):
    username = forms.CharField(label='Username', help_text='The username for the request')
    osu_user_id = forms.IntegerField(label='osu! User ID', help_text='The osu! user ID for the match the user request')

    class Meta:
        model = SignUpRequest
        fields = ['username', 'osu_user_id']