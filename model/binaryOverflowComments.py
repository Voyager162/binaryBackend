from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import datetime, timezone

class BinaryOverflowComments(db.Model):
    __tablename__ = 'binaryPostComments'
    
    # Sets the columns
    id = db.Column(db.Integer, primary_key=True)
    _post_ref = db.Column(db.Integer, db.ForeignKey('binaryPostContent.id'), nullable=False)
    _content = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # All of these are default values because they either shouldn't be controlled by user or should be the same for all posts
    _date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    
    votes = db.relationship('BinaryOverflowCommentVotes', backref='votes', cascade='all, delete-orphan')
        
    # Sets the initial parameters to create hte class
    def __init__(self, post_ref, content, author):
        self._post_ref = post_ref
        self._content = content
        self._author = author

    # String form of the class for python to interpret (?)
    def __repr__(self):
        return f'BinaryOverflowComments(id={self.id} post_ref={self._post_ref}, content={self._content}, author={self._author}, date_posted={self._date_posted})'
    
    # Creates data in databases
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    # Reads data and returns it in a dictionary/JSON format. This is to return to the frontend
    def read(self):
        votes = [vote.read() for vote in self.votes]
        upvotes = 0
        downvotes = 0
        # There's probably a more efficient way to do this but oh well
        for vote in votes:
            if vote['vote'] < 0:
                downvotes += 1
            elif vote['vote'] > 0:
                upvotes += 1
        return {
            'id': self.id,
            'post_ref': self._post_ref,
            'content': self._content,
            'author': self._author,
            'date_posted': self._date_posted.isoformat(),
            'upvotes': upvotes,
            'downvotes': downvotes
        }
    
    # Updates the data within
    def update(self, new_data):
        # Checks if the new_data is in a dictionary format
        if not isinstance(new_data, dict):
            return self
        
        content = new_data.get("content", "")
        
        # Checks if each variable exists, if they do update to the new one
        # Content is the only item that should ever be updated
        if content:
            self._blurb = content
            
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
        
    # Adds an upvote
    def upvote(self):
        pass
    
    # Adds a downvote
    def downvote(self):
        pass
        
# Initialization process        
def initBinaryComments():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = BinaryOverflowComments(post_ref=1, content="What are your guy's strategies for converting from binary to decimal?", author=1)  
        
        for post in [p1]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()