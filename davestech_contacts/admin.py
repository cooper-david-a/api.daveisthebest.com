from django.contrib import admin
from django import forms
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at", "name", "email"]
    list_per_page = 25

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "message":
            kwargs["widget"] = forms.Textarea(attrs={"rows": 10, "cols": 80})
        return super().formfield_for_dbfield(db_field, **kwargs)

