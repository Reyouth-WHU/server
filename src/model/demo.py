from models import User
from ORM import UserORM

# # INSERTING DATA
# Create adb object


# Create some User objects
Tom = User(username='a123', password='123456', email='demo@example.com')
Mike = User(username='b123', password='abcdef', email='123@example.com')
Jim = User(username='c123', password='123abc', email='123@exabmple.com')
print(Tom.username, Mike.password)

opt = UserORM()
opt.create(Tom)
opt.delete([User.id == 1])
opt.create(Mike)
opt.create(Jim)
opt.update({'username': 'hhh123'}, [User.id == 1])
print(opt.read([User.id, User.email], filter=[User.id >= 1]))
