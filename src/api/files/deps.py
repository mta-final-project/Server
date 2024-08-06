from src.services.files import S3Service


def s3_service() -> S3Service:
    return S3Service()
