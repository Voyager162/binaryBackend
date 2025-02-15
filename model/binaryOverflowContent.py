import json
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import timezone, datetime
from model.user import User

class BinaryOverflowContent(db.Model):
    __tablename__ = 'binaryPostContent'
        
    # Defined columns
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    _content = db.Column(db.String(255), nullable=False)
    
    # Defined relationships
    comments = db.relationship('BinaryOverflowComments', backref='comments', cascade='all, delete-orphan')
    votes = db.relationship('BinaryOverflowContentVotes', backref='votes', cascade='all, delete-orphan')
    
    # Initial parameters to create the class
    def __init__(self, title, author, content):
        self._title = title
        self._author = author
        self._content = content
    
    # Called when repr(object) is called. I think
    def __repr__(self):
        return f'BinaryOverflowContent(id={self.id}, title={self._title}, author={self._author}, date_posted={self._date_posted}, content={self._content})'
    
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
        user = User.query.get(self._author)
        votes = [vote.read() for vote in self.votes]
        upvotes = 0
        downvotes = 0
        # There's probably a more efficient way to do this but oh well
        if votes:
            for vote in votes:
                if vote['vote'] < 0:
                    downvotes += 1
                elif vote['vote'] > 0:
                    upvotes += 1
        return {
            'id': self.id,
            'title': self._title,
            'author': user.name if user else self._author, 
            'date_posted': self._date_posted.isoformat(),
            'content': self._content,
            'upvotes': upvotes,
            'downvotes': downvotes
        }
        
    # Updates the data inside. Only updates things that should be updated using a PUT statement
    def update(self, new_data):
        # Checks if the new_data is in a dictionary format
        if not isinstance(new_data, dict):
            return self
        
        # Gets the new data and sets it equal to these variables, these are the only things that should be changed using PUT
        title = new_data.get("title", "")
        content = new_data.get("content", "")
        
        if title:
            self._title = title
        if content: 
            self._content = content
        
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
    
    def vote(self, vote, user):
        return self.votes
        
### End Class
        
# Data Initialization
def initBinaryPostContent():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = BinaryOverflowContent(title="Binary Minithread", author=1, content="This is the megathread for binary content")
        
        for post in [p1]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()