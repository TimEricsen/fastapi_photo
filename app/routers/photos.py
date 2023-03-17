from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException, status, Query
from fastapi.responses import FileResponse
from datetime import date
from sqlalchemy.orm import Session
from typing import List, Union
import os

from .. import schemas, models
from .dependencies import get_db
from .users import get_current_user


router = APIRouter()


@router.post('/add_photo', tags=['Photo'])
async def post_photo(
        image: UploadFile = File(),
        creating_date: date = Form(default=date.today()),
        location: str = Form(),
        people: Union[List[str], None] = Form(default=None),
        current_user: schemas.UserMain = Depends(get_current_user),
        db: Session = Depends(get_db)):

    if os.path.exists(f'app/routers/photos/{image.filename}'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='This image is already exists.')

    try:
        with open(f'app/routers/photos/{image.filename}', mode='ab+') as file:
            image_in_db = models.Photo(title=image.filename,
                                       creating_date=creating_date,
                                       location=location,
                                       owner_id=current_user.id)
            db.add(image_in_db)
            db.commit()
            db.refresh(image_in_db)
            if people:
                people_list = people[0].split(',')
                for human in people_list:
                    human_in_db = models.PeopleOnPhoto(full_name=human,
                                                       photo_title=image.filename)
                    db.add(human_in_db)
                    db.commit()
                    db.refresh(human_in_db)
            file.write(image.file.read())
        return {'Info': 'Download is done!'}

    except:
        return Exception


@router.get('/photos', tags=['Photo'], response_model=List[schemas.PhotoMain])
async def get_photos(q_date: Union[date, None] = Query(default=None, example=date.today()),
                     q_location: Union[str, None] = None,
                     q_name: Union[str, None] = None,
                     db: Session = Depends(get_db)):
    photo_db = db.query(models.Photo)
    if q_date:
        photo_db = photo_db.filter(models.Photo.creating_date == q_date)
    elif q_location:
        photo_db = photo_db.filter(models.Photo.location == q_location.capitalize())
    elif q_name:
        photo_db = photo_db.join(models.PeopleOnPhoto).filter(models.PeopleOnPhoto.full_name == q_name)
    if photo_db.all() != []:
        return photo_db.all()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Photo with this filter(s) not found'
        )


@router.get('/photos/{photo_id}', tags=['Photo'])
async def get_photo(photo_id: int,
                    db: Session = Depends(get_db)):
    photo_db = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if photo_db:
        return FileResponse(f'app/routers/photos/{photo_db.title}')
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Photo with id {photo_id} not found')


@router.get('/names/{name}', tags=['Photo'])
async def name_like(name: str,
                    db: Session = Depends(get_db)):
    name_in_db = db.query(models.PeopleOnPhoto).filter(models.PeopleOnPhoto.full_name.ilike(f'%{name}%')).all()
    if name_in_db:
        return name_in_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='This name was not found')

