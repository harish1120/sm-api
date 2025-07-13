from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import oauth2, schemas
import app.db_tables as models

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
    responses={404: {"description": "Not found"}}
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def voting(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {vote.post_id} does not exist")
    
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, 
                                               models.Votes.user_id == current_user.id).filter()
    
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote: 
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, 
                                detail="User has already voted for the post")
        
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added succefully"}
    
    else:
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}
