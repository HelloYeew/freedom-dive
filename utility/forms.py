from django import forms


class ImportSpecificBeatmapSetForm(forms.Form):
    beatmapset_id = forms.IntegerField(label='Beatmapset ID', help_text='The ID of the beatmapset you want to import.')

    class Meta:
        fields = ['beatmapset']