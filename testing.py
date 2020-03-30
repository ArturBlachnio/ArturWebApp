from awa import db
db.create_all()


from awa.iplan.models import Post

Post.query.all()



db.create_all()