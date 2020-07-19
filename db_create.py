from app import db
from models import BlogPost

db.drop_all()
# Create the database and the db tables
db.create_all()

# Insert
post_1 = BlogPost(title="Good", description="I'm good!")

post_2 = BlogPost(title="Well", description="I'm Well!")

db.session.add(post_1)
db.session.add(post_2)

# Commit to db

db.session.commit()
