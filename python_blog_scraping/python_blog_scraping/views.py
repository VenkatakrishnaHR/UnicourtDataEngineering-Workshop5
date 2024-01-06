import time

from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .tasks import extract_blogs
from .models import ExtractionRequest, Blog
from .constants import ExtractionStatus, APIFields, APIObjectNames, APIErrorResponses, APIErrorCodes


@method_decorator(csrf_exempt, name='dispatch')
class GetArticlesByReleaseDate(View):

    def get(self, request, articleReleaseDate):
        articles_for_release_date = Blog.objects.filter(
            release_date=articleReleaseDate
        )

        article_response_list = []
        for article in articles_for_release_date:
            article_response_list.append({
                "object": "Article",
                "title": article.title,
                "releaseDate": article.release_date,
                "author": article.author,
                "blogTime": article.blog_time,
                "ReleaseDate": article.created_date
            })

        response_dict = {
            "object": "ArticlesByReleaseDate",
            "articleReleaseDate": articleReleaseDate,
            "articlesByReleaseDateArray": article_response_list,
            "nextPageAPI": None,
            "totalPages": 1,
            "totalCount": len(article_response_list)
        }

        return JsonResponse(response_dict, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ExtractBlogByReleaseDate(View):

    def post(self, request):
        start_date = request.GET.get('articleReleaseStartDate', None)
        end_date = request.GET.get('articleReleaseEndDate', None)

        print(start_date)
        print(end_date)

        extraction_request_id = f"ARDR{int(time.time())}"
        extraction_request_obj = ExtractionRequest(
            extractionRequestId=extraction_request_id,
            start_date=start_date,
            end_date=end_date,
            status=ExtractionStatus.IN_PROGRESS
        )
        extraction_request_obj.save()
        extract_blogs.apply_async(kwargs=dict(extraction_request_id=extraction_request_id), queue="extract")

        return JsonResponse(
            {
                APIFields.OBJECT: APIObjectNames.EXTRACT_ARTICLE_BY_RELEASE_DATE_REQUEST,
                APIFields.EXTRACTION_REQUEST_ID: extraction_request_id,
                APIFields.STATUS: ExtractionStatus.IN_PROGRESS
            },
            status=200
        )

    def get(self, request, extractionRequestId):
        try:
            extraction_request_obj: ExtractionRequest = ExtractionRequest.objects.get(
                extractionRequestId=extractionRequestId
            )
            response_dict = {
                APIFields.OBJECT: APIObjectNames.EXTRACT_ARTICLE_BY_RELEASE_DATE_REQUEST,
                APIFields.EXTRACTION_REQUEST_ID: extraction_request_obj.extractionRequestId,
                APIFields.STATUS: extraction_request_obj.status
            }
        except ExtractionRequest.DoesNotExist:
            response_dict = {
                APIFields.OBJECT: APIObjectNames.EXCEPTION,
                APIFields.CODE: APIErrorCodes.ERROR_CODE_404,
                APIFields.MESSAGE: APIErrorResponses.RESOURCE_NOT_FOUND,
                APIFields.DETAILS: APIErrorResponses.NO_RESULT_FOUND_FOR_EXTRACTION_REQUEST_ID,
            }

        return JsonResponse(response_dict, status=200)


def python_blog_scraping(request, job_id):
    return redirect('/admin/members/job/')
