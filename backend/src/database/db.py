from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import models

def get_challenge_quota(db: Session, user_id: str):
    """
    Retrieve the challenge quota for a specific user.
    
    :param db: Database session
    :param user_id: ID of the user
    :return: ChallengeQuota object or None if not found
    """
    return (db.query(models.ChallengeQuota)
            .filter(models.ChallengeQuota.user_id == user_id)
            .first())

def create_challenge_quota(db: Session, user_id: str):
    """
    Create a new challenge quota for a specific user.
    
    :param db: Database session
    :param user_id: ID of the user
    :return: Created ChallengeQuota object
    """
    db_quota = models.ChallengeQuota(user_id=user_id)
    db.add(db_quota)
    db.commit()
    db.refresh(db_quota)
    return db_quota

def reset_quota_if_needed(db: Session, quota: models.ChallengeQuota):
    """ Check if the quota needs to be reset and reset it if necessary.
    :param db: Database session
    :param quota: ChallengeQuota object
    :return: Updated ChallengeQuota object
    """
    now = datetime.now()
    if now - quota.last_reset_date > timedelta(hours=24):
        quota.quota_remaining = 10
        quota.last_reset_date = now
        db.commit()
        db.refresh(quota)
    return quota

def create_challenge(
        db: Session, 
        difficulty: str,
        created_by: str,
        title: str,
        options: str,
        correct_answer_id: int,
        explanation: str
):
    """ Create a new challenge in the database.
    :param db: Database session
    :param difficulty: Difficulty level of the challenge
    :param created_by: ID of the user who created the challenge
    :param title: Title of the challenge
    :param options: Answer options for the challenge
    :param correct_answer_id: ID of the correct answer
    :param explanation: Explanation for the correct answer
    :return: Created Challenge object
    """
    db_challenge = models.Challenge(
        difficulty=difficulty,
        created_by=created_by,
        title=title,
        options=options,
        correct_answer_id=correct_answer_id,
        explanation=explanation
    )

    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge
                     
def get_user_challenges(db: Session, user_id: str):
    """
    Retrieve all challenges created by a specific user.
    
    :param db: Database session
    :param user_id: ID of the user
    :return: List of Challenge objects
    """
    print("Fetching user challenges for user_id:", user_id)
    return db.query(models.Challenge).filter(models.Challenge.created_by == user_id).all()