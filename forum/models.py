from django.db import models
from django.urls import reverse


from user_management.models import Profile


class ThreadCategory(models.Model):
    '''
    This is the model for the Thread categories.

    The name is the character field for the name of the category
    The description is text field for the explanation of the category
    '''
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('forum:thread_category', args=[str(self.name)])

    class Meta:
        '''
        The Thread categories are ordered based on name in ascending order

        The name of the thread model as it appears on the admin page is Thread Category for single,
        and Thread Categories for plural
        '''
        ordering = ['name']
        verbose_name = 'Thread Category'
        verbose_name_plural = 'Thread Categories'


class Thread(models.Model):
    '''
    The model for the Thread

    The title is the character field for the title of the thread
    The author is the foreign key connected to the user who created the thread
    The category is the existing category that the thread is under
    The entry is the text field that represents the entry text of the thread
    The image is the optional image attached to the thread
    The created_on field is date time field that shows the date and time 
    the thread is created on
    The updated_on field is date time field updated_on is the date time field
    that shows the date and time the thread gets updated
    '''
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="threads"
    )
    category = models.ForeignKey(
        ThreadCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="threads"
    )
    entry = models.TextField(null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:thread_detail', args=[str(self.pk)])

    class Meta:
        '''
        The threads are ordered based on the date and time they were created on, and 
        with the most recent first

        The name of the thread model as it appears on the admin page is Thread for single,
        and Threads for plural
        '''
        ordering = ['-created_on',]
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'


class Comment(models.Model):
    '''
    The model for the Comments

    The thread is the foreign key of the thread that it is connected to 
    The author is the foreign key of the user who created the comment
    The entry field is the text field that shows the entry 
    The created_on field is the date time field that stores the time the thread was created
    The updated_on field is the date time field that stores the time the thread was updated
    '''
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="comments", null=True,
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments",
    )
    entry = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entry

    class Meta:
        '''
        The comments are ordered based on the date and time they were created on, and 
        with the most recent last

        The name of the thread model as it appears on the admin page is Comment for single,
        and Comments for plural
        '''
        ordering = ('-created_on',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


# Create your models here.
