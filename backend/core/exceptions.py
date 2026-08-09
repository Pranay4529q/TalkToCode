from fastapi import HTTPException, status


class RepoNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Repo not found")


class RepoNotReadyError(HTTPException):
    def __init__(self, current_status: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repo is not ready for chat yet (status: {current_status})",
        )


class IngestionError(HTTPException):
    def __init__(self, reason: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ingestion failed: {reason}")
