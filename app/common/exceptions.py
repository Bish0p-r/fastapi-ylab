from fastapi import HTTPException, status

MenuWithThisTitleExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='A menu with this title already exists.'
)

MenuNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')

SubMenuWithThisTitleExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='A submenu with this title already exists.'
)

SubMenuNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')

DishWithThisTitleExists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail='A dish with this title already exists.'
)

DishNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')
