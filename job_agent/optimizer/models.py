from django.db import models


class EmbeddingDoc(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    text = models.TextField()
    vector_json = models.TextField()  # store JSON-encoded list[float]
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"EmbeddingDoc(id={self.id}, title={self.title})"
from django.contrib.auth.models import User

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    skills = models.TextField(blank=True, null=True)  # comma-separated or JSON
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    raw_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume - {self.user.username}"


class OptimizedResume(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    optimized_file = models.FileField(upload_to='optimized_resumes/')
    ats_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    improvement_summary = models.TextField(blank=True, null=True)
    generated_cover_letter = models.TextField(blank=True, null=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Optimized Resume for {self.resume.user.username} ({self.job_posting.title})"
