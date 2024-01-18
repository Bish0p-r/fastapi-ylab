from fastapi import HTTPException, status


MenuWithThisTitleExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="A menu with this title already exists."
)
