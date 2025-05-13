from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from user_management.models import Profile


class Commission(models.Model):
    '''
    Represents a commission/task with jobs

    connected to a Profile model to represent the author of the commission
    '''
    # status - character from A-D - represents Open, Full, Completed, or Discontinued - alphabetical characters used for easy ordering
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
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='commissions', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=OPEN)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:commission-detail', args=[self.pk])

    class Meta():
        ordering = ['status', 'created']
        verbose_name = "Commission"


class Job(models.Model):
    '''
    Represents a job users can apply to

    connected to a commission model as the job is posted under a commission
    '''
    # status - character A or B - represents Open or Full - alphabetical characters used for easy ordering
    
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
        default=1, validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=OPEN)

    def __str__(self):
        return self.role

    class Meta():
        ordering = ['status', '-manpowerRequired']
        verbose_name = "Job"


class JobApplication(models.Model):
    '''
    Represents a user's application for a job posted under commission

    connected to the Job model as the job the applicant is applying to and the Profile model as the user who applied
    '''
    # status - character from A-C - represents Pending, Accepted, or Rejected - alphabetical characters used for easy ordering
    PENDING = "A"
    ACCEPTED = "B"
    REJECTED = "C"
    STATUS_CHOICES = {
        PENDING: "Pending",
        ACCEPTED: "Accepted",
        REJECTED: "Rejected",
    }
    job = models.ForeignKey(Job, on_delete=models.CASCADE,
                            related_name='applications')
    applicant = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='job_applications')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    appliedOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.role

    class Meta():
        ordering = ['status', '-appliedOn']
        verbose_name = "Job Application"
