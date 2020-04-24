from models import User
from ORM import UserORM

# # INSERTING DATA
# Create adb object


# Create some User objects
Tom = User(username='a123', password='123456', email='demo@example.com')
Mike = User(username='b123', password='abcdef', email='123@example.com')
Jim = User(username='c123', password='123abc', email='123@exabmple.com')
print(Tom.username, Mike.password)

UserORM.create(Tom)
UserORM.delete([User.id == 1])
UserORM.create(Mike)
UserORM.create(Jim)
UserORM.update({'username': 'hhh123'}, [User.id == 1])
print(UserORM.read([User.id, User.email], filter=[User.id >= 1]))
