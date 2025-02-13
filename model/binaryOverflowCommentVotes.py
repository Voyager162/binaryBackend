from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import timezone, datetime

class BinaryOverflowCommentVotes(db.Model):
    __tablename__ = 'binaryPostCommentVotes'
        
    # Defined columns
    id = db.Column(db.Integer, primary_key=True)
    _post_id = db.Column(db.String(255), db.ForeignKey('binaryPostComments.id'), nullable=False)
    _user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _vote = db.Column(db.Integer, nullable=False)
    
    # Initial parameters to create the class
    def __init__(self, post_id, user, vote):
        self._post_id = post_id
        self._user = user
        self._vote = vote
    
    # Called when doing repr(object). I think
    def __repr__(self):
        return f'BinaryOverflowCommentVotes(id={self.id}, post_id={self._post_id}, user={self._user}, vote={self._vote})'
    
    # Create a new post object
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e        

    # Reads the data and returns it in a dictionary, key-pair value format
    def read(self):
        return {
            'id': self.id,
            'post_id': self._post_id,
            'user': self._user,
            'vote': self._vote
        }
        
    def update(self, new_data):
        if not isinstance(new_data, dict):
            return self
        
        vote = new_data.get('vote', '')
        if self._vote == vote:
            self._vote = 0
        else:
            self._vote = vote
               
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    # Deletes the data
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e