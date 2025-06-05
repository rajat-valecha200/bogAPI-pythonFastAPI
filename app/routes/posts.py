from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is Invalid")
    
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=list[schemas.PostOut])
def get_all_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).all()

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")
    return post

@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, updated: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in updated.dict().items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_d != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(post)
    db.commit()
    return {"message":"Post deleted"}

@router.post("/upload/")
def upload_image(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return {"filename":file.filename}