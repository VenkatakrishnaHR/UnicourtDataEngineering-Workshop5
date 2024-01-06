from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=500)
    release_date = models.DateTimeField('Realse Date')
    blog_time = models.CharField(max_length=50)
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField('Created Date', auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class ExtractionRequest(models.Model):
    extractionRequestId = models.CharField(max_length=14)
    start_date = models.DateTimeField('Blog start date', null=True)
    end_date = models.DateTimeField('Blog end date', null=True)
    status = models.CharField('Extraction Status', null=False)

    def __str__(self):
        return self.extractionRequestId


class Job(models.Model):
    job_name = models.CharField(max_length=500)
    start_date = models.DateTimeField('Blog start date', null=True)
    end_date = models.DateTimeField('Blog end date', null=True)
    start_no = models.IntegerField(verbose_name="No of blogs to skip", null=True)
    no_of_blogs = models.IntegerField(verbose_name="No of blogs to extract", null=True)
    created_date = models.DateTimeField('Job created date', auto_now_add=True, null=True)

    def __str__(self):
        return self.job_name


class JobStats(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    total_blogs = models.IntegerField(verbose_name="Total blogs found", null=True)
    no_of_blogs_extracted = models.IntegerField(verbose_name='No of blogs extracted', null=True)
    start_date = models.DateTimeField('Extraction start date', null=True)
    end_date = models.DateTimeField('Extraction start date', null=True)

    def __str__(self):
        return self.job.job_name


class JobLogs(models.Model):
    job_stats = models.ForeignKey(JobStats, on_delete=models.CASCADE)
    log = models.TextField(verbose_name="job logs")
    function_name = models.TextField(verbose_name="Function name")
    date = models.DateTimeField('Log date', null=True, auto_now_add=True)
