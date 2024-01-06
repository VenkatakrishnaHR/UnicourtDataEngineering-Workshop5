class ExtractionStatus:
    IN_PROGRESS = "IN PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class APIFields:
    OBJECT = "object"
    EXTRACTION_REQUEST_ID = "extractionRequestId"
    STATUS = "status"
    CODE = "code"
    MESSAGE = "message"
    DETAILS = "details"


class APIObjectNames:
    EXTRACT_ARTICLE_BY_RELEASE_DATE_REQUEST = "ExtractArticleByReleaseDateRequest"
    EXCEPTION = "Exception"


class APIErrorCodes:
    ERROR_CODE_400 = "UN400"
    ERROR_CODE_404 = "UN404"


class APIErrorResponses:
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"

    INVALID_EXTRACTION_REQUEST_ID = "Requested extractionRequestId is invalid."
    NO_RESULT_FOUND_FOR_EXTRACTION_REQUEST_ID = "No result found for requested extractionRequestId."
