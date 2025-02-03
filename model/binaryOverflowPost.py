from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db

class BinaryOverflowPost(db.Model):
    __tablename__ = 'binaryPosts'
    
    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    # Place binaryPostContent Id here
    _post_ref = db.Column(db.Integer, db.ForeignKey('binaryPostContnet._post_id'), nullable=False)
    _blurb = db.Column(db.String(255), nullable=False)
    _author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _date_posted = db.Column(db.String(255), nullable=False)
    
    # # WIP Features
    # _upvotes = db.Column(db.Integer, nullable=False)
    # _downvotes = db.Column(db.Integer, nullable=False)
    # _users_upvoted = db.Column()
    # _users_downvoted = db.Column()
    
    def __init__(self, title, post_ref, blurb, author, date_posted):
        self._title = title
        self._post_ref = post_ref
        self._blurb = blurb
        self._author = author
        self._date_posted = date_posted

    def __repr__(self):
        return f'BinaryOverflowPosts(id={self.id}, title={self._title}, post_ref={self._post_ref}, blurb={self._blurb}, author={self._author}, date_posted={self._date_posted})'
    
    def create(self):
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
            'post_ref': self._post_ref,
            'blurb': self._blurb,
            'author': self._author,
            'date_posted': self._date_posted
        }
        
    def update(self, new_data):
        # Checks if the new_data is in a dictionary format
        if not isinstance(new_data, dict):
            return self
        
        # Gets the new data and sets it equal to these variables
        title = new_data.get("title", "")
        post_ref = new_data.get("post_ref", "")
        blurb = new_data.get("blurb", "")
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
        
def initBinaryPosts():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = BinaryOverflowPost(title='Binary Megathread', post_ref=1, blurb="placeholder", author=1, date_posted="2024/02/24")  
        p2 = BinaryOverflowPost(title='Binary Minithread', post_ref=2, blurb="placeholder", author=1, date_posted="2024/02/24")  
        
        for post in [p1, p2]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()