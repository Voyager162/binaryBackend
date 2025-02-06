from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from datetime import timezone, datetime

class BinaryOverflowContent(db.Model):
    __tablename__ = 'binaryPostContent'
        
    # Defined columns
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    _content = db.Column(db.String(255), nullable=False)
    _upvotes = db.Column(db.Integer, nullable=False, default=0)
    _downvotes = db.Column(db.Integer, nullable=False, default=0)
    _users_voted = db.Column(db.JSON, nullable=True, default=None)
    
    # Defined relationships
    comments = db.relationship('BinaryOverflowComments', backref='comments', cascade='all, delete-orphan')
    
    # Initial parameters to create the class
    def __init__(self, title, author, content):
        self._title = title
        self._author = author
        self._content = content
    
    # Called when initally created (?). I think
    def __repr__(self):
        return f'BinaryOverflowContent(id={self.id}, title={self._title}, author={self._author}, date_posted={self._date_posted}, content={self._content}, upvotes={self._upvotes}, downvotes={self._downvotes}, users_voted={self._users_voted})'
    
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
            'title': self._title,
            'author': self._author,
            'date_posted': self._date_posted.isoformat(),
            'content': self._content,
            'upvotes': self._upvotes,
            'downvotes': self._downvotes,
            'users_voted': self._users_voted            
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
    
    # Adds an upvote
    def upvote(self):
        # WIP NOT DONE
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    # Adds a downvote
    def downvote(self):
        # WIP NOT DONE
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e 
        
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