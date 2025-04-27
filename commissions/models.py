from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from user_management.models import Profile


class Commission(models.Model):
    OPEN = "A"
    FULL = "B"
    COMPLETED = "C"
    DISCONTINUED = "D"
    STATUS_CHOICES = {
        OPEN: "Open",
        FULL: "Full",
        COMPLETED: "Completed",
        DISCONTINUED: "Discountinued",
    }
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='commissions',null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=OPEN)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

    class Meta():
        ordering = ['status','created']
        verbose_name = "Commission"


class Job(models.Model):
    OPEN = "A"
    FULL = "B"
    STATUS_CHOICES = {
        OPEN: "Open",
        FULL: "Full",
    }
    commission = models.ForeignKey(
        Commission, on_delete=models.CASCADE, related_name='jobs')
    role = models.TextField(blank=True)
    manpowerRequired = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=OPEN)
    
    def __str__(self):
        return self.role

    class Meta():
        ordering = ['status','-manpowerRequired']
        verbose_name = "Job"


class JobApplication(models.Model):
    PENDING = "A"
    ACCEPTED = "B"
    REJECTED = "C"
    STATUS_CHOICES = {
        PENDING: "Pending",
        ACCEPTED: "Accepted",
        REJECTED: "Rejected",
    }
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=PENDING)
    appliedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.role

    class Meta():
        ordering = ['status','-appliedOn']
        verbose_name = "Job Application"
        
