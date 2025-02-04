from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.binaryOverflowContent import BinaryOverflowContent
from datetime import datetime, timezone
class BinaryOverflowPost(db.Model):
    __tablename__ = 'binaryPosts'
    
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _post_ref = db.Column(db.Integer, db.ForeignKey('binaryPostContent.id'), nullable=False)
    _blurb = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    _upvotes = db.Column(db.Integer, nullable=False)
    _downvotes = db.Column(db.Integer, nullable=False)
    _users_voted = db.Column(db.JSON, nullable=True)
    
    # HOW TO QUERY WITHOUT REFERENCING ID
    # # Get posts created after a specific date
    # specific_date = datetime(2025, 1, 1)
    # posts = Post.query.filter(Post.created_at > specific_date).all()
    # # Get posts updated after a specific date
    # recent_posts = Post.query.filter(Post.updated_at > datetime(2025, 2, 1)).all()
        
    def __init__(self, post_ref):
        self._post_ref = post_ref
        post = BinaryOverflowContent.query.get(self._post_ref)
        self._title = post._title if post else None
        self._blurb = post._content if post else None
        self._author = post._author if post else None
        self._upvotes = post._upvotes if post else None
        self._downvotes = post._downvotes if post else None
        self._users_voted = post._users_voted if post else None

    def __repr__(self):
        return f'BinaryOverflowPosts(id={self.id}, title={self._title}, post_ref={self._post_ref}, blurb={self._blurb}, author={self._author}, date_posted={self._date_posted}, upvotes={self._upvotes}, downvotes={self._downvotes}, users_voted={self._users_voted})'
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def read(self):
        post = BinaryOverflowContent.query.get(self._post_ref)
        return {
            'id': self.id,
            'title': post.title if post else None,
            'post_ref': post.post_id if post else None,
            'blurb': post.content if post else None,
            'author': post.author if post else None,
            'date_posted': self._date_posted,
            'upvotes': post.upvotes if post else None,
            'downvotes': post.downvotes if post else None,
            'users_voted': post.users_voted if post else None
        }
        
    def update(self, new_data):
        # Checks if the new_data is in a dictionary format
        if not isinstance(new_data, dict):
            return self
        
        # Gets the new data and sets it equal to these variables
        title = new_data.get("title", "")
        # Should never need to be updated, as it referenced post should always be same
        post_ref = new_data.get("post_ref", "")
        blurb = new_data.get("blurb", "")
        # Update when user changes name, shouldn't be necessary with current implementation
        author = new_data.get("author", "")
        # This shouldn't ever need to be updated but will be added just in case
        date_posted = new_data.get("date_posted", "")
        
        # Checks if each variable exists, if they do update to the new one
        if title:
            self._title = title
        if post_ref:
            self._post_ref = post_ref
        if blurb:
            self._blurb = blurb
        if author:
            self._author = author
        if date_posted:
            self._date_posted = date_posted
            
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
        
# Initialization process        

def initBinaryPosts():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = BinaryOverflowPost(post_ref=1)  
        
        for post in [p1]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()