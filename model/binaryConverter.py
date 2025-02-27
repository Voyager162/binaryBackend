from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db

class BinaryConverter(db.Model):
    """
    BinaryConverter Model
    
    Represents a binary-to-decimal conversion record.
    """
    __tablename__ = 'binaryConverter'

    id = db.Column(db.Integer, primary_key=True)
    binary = db.Column(db.String(255), nullable=False)
    decimal = db.Column(db.String(255), nullable=False)

    def __init__(self, binary, decimal):
        """
        Constructor for BinaryConverter.
        """
        self.binary = binary
        self.decimal = decimal

    def __repr__(self):
        """
        Represents the BinaryConverter object as a string for debugging.
        """
        return f"<BinaryConverter(id={self.id}, binary='{self.binary}', decimal='{self.decimal}')>"

    def create(self):
        """
        Adds the record to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Returns the binary-to-decimal conversion details as a dictionary.
        """
        return {
            "id": self.id,
            "binary": self.binary,
            "decimal": self.decimal,
        }

    def update(self, data):
        """
        Updates the record with new data and commits the changes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Deletes the record from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        existing_sections = {section.id: section for section in BinaryConverter.query.all()}
        for section_data in data:
            _ = section_data.pop('id', None)  # Remove 'id' from section_data
            binary = section_data.get("binary", None)
            section = existing_sections.pop(binary, None)
            if section:
                section.update(section_data)
            else:
                section = BinaryConverter(**section_data)
                section.create()
        
        # Remove any extra data that is not in the backup
        for section in existing_sections.values():
            db.session.delete(section)
        
        db.session.commit()
        return existing_sections

def initBinaryConverter():
    """
    Initializes the BinaryConverter table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables

        # Sample test data
        quizzes = [
            BinaryConverter(decimal="1", binary="1"),
            BinaryConverter(decimal="2", binary="10"),
            BinaryConverter(decimal="3", binary="11"),
            BinaryConverter(decimal="4", binary="100"),
            BinaryConverter(decimal="5", binary="101"),
            BinaryConverter(decimal="6", binary="110"),
            BinaryConverter(decimal="7", binary="111"),
            BinaryConverter(decimal="8", binary="1000"),
            BinaryConverter(decimal="9", binary="1001"),
            BinaryConverter(decimal="10", binary="1010"),
            BinaryConverter(decimal="11", binary="1011"),
            BinaryConverter(decimal="12", binary="1100"),
            BinaryConverter(decimal="13", binary="1101"),
            BinaryConverter(decimal="14", binary="1110"),
            BinaryConverter(decimal="15", binary="1111"),
            BinaryConverter(decimal="16", binary="10000"),
            BinaryConverter(decimal="17", binary="10001"),
            BinaryConverter(decimal="18", binary="10010"),
            BinaryConverter(decimal="19", binary="10011"),
            BinaryConverter(decimal="20", binary="10100"),
        ]

        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {quiz}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {quiz}")
