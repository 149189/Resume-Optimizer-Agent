from django.contrib import admin
from .models import JobPosting, Resume, OptimizedResume

admin.site.register(JobPosting)
admin.site.register(Resume)
admin.site.register(OptimizedResume)
