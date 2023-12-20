from django.db import models


class Paper(models.Model):
    title = models.TextField()
    keywords = models.TextField()
    citation_count = models.IntegerField()
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    type = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    volume = models.CharField(max_length=20)
    issue = models.CharField(max_length=20)
    issn = models.CharField(max_length=20)
    isbn = models.CharField(max_length=20)
    doi = models.CharField(max_length=20)
    pdf_link = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    abstract = models.TextField()
    last_update_time = models.DateTimeField(null=True)
    venue_id = models.IntegerField()



class Patent(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    title = models.TextField()
    keywords = models.TextField()
    citation_count = models.IntegerField()
    page_start = models.IntegerField()
    page_end = models.IntegerField()
    type = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    volume = models.CharField(max_length=20)
    issue = models.CharField(max_length=20)
    pdf_link = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    abstract = models.TextField()
    last_update_time = models.DateTimeField()
    venue_id = models.IntegerField()


class Work_Data(models.Model):
    browse_times = models.IntegerField(default=0)
    work_id = models.CharField('work_id',max_length=40)
    title = models.CharField('title',max_length=40)
