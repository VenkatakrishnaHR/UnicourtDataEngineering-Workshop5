import datetime
from .celery import app
from .models import Job, Blog, JobStats, JobLogs, ExtractionRequest
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import pytz
from .constants import ExtractionStatus


utc=pytz.UTC


@app.task(bind=True, name="extract")
def extract_blogs(task_obj, extraction_request_id):
    extraction_request_obj = ExtractionRequest.objects.get(extractionRequestId=extraction_request_id)
    try:
        job_obj, is_created = Job.objects.get_or_create(
            start_date=extraction_request_obj.start_date,
            end_date=extraction_request_obj.end_date,
        )

        if is_created:
            job_obj.job_name = f"{extraction_request_obj.start_date.date()} to {extraction_request_obj.end_date.date()}"
            job_obj.save()

        job_stats_obj = JobStats(job=job_obj, status="IN PROGRESS", start_date=datetime.datetime.now(), no_of_blogs_extracted=0)
        job_stats_obj.save()
        JobLogs(job_stats=job_stats_obj, log="Extraction stated", function_name="extract", date=datetime.datetime.now()).save()
        start_date = job_obj.start_date
        end_date = job_obj.end_date

        url = "https://blog.python.org/"
        article_count = 0

        data = requests.get(url)
        page_soup = BeautifulSoup(data.text, 'html.parser')

        blogs = page_soup.select('div.date-outer')
        counter = 0
        for blog in blogs:
            article_count += 1
            date = blog.select('.date-header span')[0].get_text()

            converted_date = parse(date)
            JobLogs(job_stats=job_stats_obj, log=f"Extracting {article_count}", function_name="extract", date=datetime.datetime.now()).save()
            if start_date and utc.localize(converted_date) < start_date:
                continue
            if end_date and utc.localize(converted_date) > end_date:
                continue

            post = blog.select('.post')[0]

            title_bar = post.select('.post-title')
            if len(title_bar) > 0:
                title = title_bar[0].text
            else:
                title = post.select('.post-body')[0].contents[0].text

            # getting the author and blog time
            post_footer = post.select('.post-footer')[0]

            author = post_footer.select('.post-author span')[0].text

            time = post_footer.select('abbr')[0].text

            blog_obj, is_created = Blog.objects.get_or_create(title=title, author=author, release_date=converted_date, blog_time=time)
            blog_obj.save()
            job_stats_obj.no_of_blogs_extracted += 1
            job_stats_obj.save()

            print("\nTitle:", title.strip('\n'))
            print("Date:", converted_date, )
            print("Time:", time)
            print("Author:", author)
            counter += 1
        JobLogs(job_stats=job_stats_obj, log=f"Total {counter} articles extracted: ", function_name="extract", date=datetime.datetime.now()).save()
        job_stats_obj.end_date = datetime.datetime.now()
        job_stats_obj.total_blogs = article_count
        job_stats_obj.status = ExtractionStatus.COMPLETED
        job_stats_obj.save()

        extraction_request_obj.status = ExtractionStatus.COMPLETED
        extraction_request_obj.save()

        JobLogs(job_stats=job_stats_obj, log="Extraction Done", function_name="extract", date=datetime.datetime.now()).save()
    except Exception as ex:
        JobLogs(job_stats=job_stats_obj, log=str(ex), function_name="extract", date=datetime.datetime.now()).save()
        job_stats_obj.end_date = datetime.datetime.now()
        job_stats_obj.total_blogs = article_count
        job_stats_obj.status = ExtractionStatus.FAILED
        job_stats_obj.save()
        JobLogs(job_stats=job_stats_obj, log="Extraction Done", function_name="extract", date=datetime.datetime.now()).save()

        extraction_request_obj.status = ExtractionStatus.FAILED
        extraction_request_obj.save()
