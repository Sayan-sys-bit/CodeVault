from django.db import models


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    author = models.CharField(max_length=50)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    pdf = models.FileField(
    upload_to='programming_pdfs/',
    blank=True,
    null=True
    )

    def __str__(self):
        return self.title + ' - ' + self.author


class CommunityResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='community_resources/')
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title