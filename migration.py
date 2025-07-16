from sqlalchemy.orm import Session
from app import models, utils, database  # adjust import according to your project structure

def hash_existing_passwords():
    db: Session = next(database.get_db())

    users = db.query(models.User).all()

    for user in users:
        # crude check if password is hashed (bcrypt hashes start with $2b$)
        if not user.password.startswith("$2b$"):
            print(f"Hashing password for user {user.email}")
            user.password = utils.hash(user.password)
            db.add(user)

    db.commit()
    db.close()

if __name__ == "__main__":
    hash_existing_passwords()
