from django.contrib import admin
from .models import Doctor, Post




class CustomDoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name','last_name', 'verification_status','email','rating', )
    list_display_links = ('user',)
    list_editable = ('verification_status',)
    list_filter = ('verification_status','email')
    search_fields = ('user__username', 'email', 'first_name','last_name',)
    readonly_fields = ('date_of_birth',)

    fieldsets = (
        ('User Information', {
            'fields': ('user','first_name','last_name', 'phone_number','email','specialization','city','years_of_experience','languages',),
        }),
        ('Verification Information', {
            'fields':('national_id_or_passport_image','passport_or_id_number','medical_licence','date_of_birth','date_issued','expiry_date','verification_status', ),
            'classes': ('wide',),
        }),
    )
admin.site.register(Doctor, CustomDoctorAdmin)
admin.site.register(Post)