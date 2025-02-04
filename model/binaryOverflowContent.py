from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db

class BinaryOverflowContent(db.Model):
    __tablename__ = 'binaryPostContent'
    
    # IDEA FOR CREATING POST_ID. ADD ALL CURRENTLY EXISTING POST_ID TO A LIST AND .MAX() IT. (may need to convert to decimal first)
    
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _post_id = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Plan is for two types, either parent or child. If it's a child make sure to include the parent
    _state = db.Column(db.String(255), nullable=False)
    _parent = db.Column(db.Integer, nullable=True, default=None)
    _content = db.Column(db.String(255), nullable=False)
    _upvotes = db.Column(db.Integer, nullable=False, default=0)
    _downvotes = db.Column(db.Integer, nullable=False, default=0)
    _users_voted = db.Column(db.JSON, nullable=True, default=None)
    
    def __init__(self, title, post_id, author, state, content, parent=None):
        self._title = title
        self._post_id = post_id
        self._author = author
        self._state = state
        self._parent = parent
        self._content = content
    
    def __repr__(self):
        return f'BinaryOverflowContent(id={self.id}, title={self._title}, post_id={self._post_id}, author={self._author} state={self._state}, parent={self._parent}, content={self._content}, upvotes={self._upvotes}, downvotes={self._downvotes}, users_voted={self._users_voted})'
    
    def create(self):
        # Create a new post object, this is to make building the page easier
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def read(self):
        return {
            'id': self.id,
            'title': self._title,
            'post_id': self._post_id,
            'author': self._author,
            'state': self._state,
            'parent': self._parent,
            'content': self._content,
            'upvotes': self._upvotes,
            'downvotes': self._downvotes,
            'users_voted': self._users_voted            
        }
        
    def update(self, new_data):
        # Checks if the new_data is in a dictionary format
        if not isinstance(new_data, dict):
            return self
        
        # Gets the new data and sets it equal to these variables
        title = new_data.get("title", "")
        post_id = new_data.get("post_id", "")
        ### These two values should never need to be updated, so please don't
        state = new_data.get("state", "")
        parent = new_data.get("parent", "")
        ###
        content = new_data.get("content", "")
        
        if title:
            self._title = title
        if post_id:
            self._post_id = post_id
        if state:
            self._state = state
        if parent:
            self._parent = parent
        if content: 
            self._content = content
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
def initBinaryPostContent():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = BinaryOverflowContent(title="Binary Minithread", post_id="000000", author=1,state="parent", content="This is the megathread for binary content")
        
        for post in [p1]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()