import os
import sys
sys.path.append(os.getcwd()+"/app")

from webapp.auth.UserRepository import UserRepository
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# database is memory only, for testing purposes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'
    
    def __str__(self):
        return self.name

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create some sample users with custom roles
    user_repo = UserRepository(User, db)
    roles = ['admin', 'user', 'guest', 'manager', 'developer']
    for i in range(5):
        name = f'User {i+1}'
        email = f'user{i+1}@example.com'
        role = roles[i % len(roles)]
        user_repo.create(name=name, email=email, role=role)

    # Get all users
    all_users = user_repo.get_all()
    print(f"All users: {all_users}")

    # Get a user by ID
    user = user_repo.get_by_id(1)
    print(f"User with ID 1: {user}")

    # Update a user
    user_repo.update(user.id, name="John Smith", email="john.smith@example.com")
    updated_user = user_repo.get_by_id(1)
    print(f"Updated user: {updated_user}")
    # Get all users again
    all_users = user_repo.get_all()
    print(f"All users: {all_users}")

    # Delete a user
    if user_repo.delete(updated_user.id):
        print(f"Deleted user: {updated_user}")
    else:
        print(f"Failed to delete user: {updated_user}")
    # Get all users again
    all_users = user_repo.get_all()
    print(f"All users: {all_users}")

    # Delete non-existing user
    if user_repo.delete(updated_user.id):
        print(f"Deleted user: {updated_user}")
    else:
        print(f"Failed to delete user: {updated_user}")
    # Get all users again
    all_users = user_repo.get_all(sort_by='name', per_page=2)
    print(f"All users: {all_users.items}")

    # Get all managers
    admin_users = user_repo.get_users_by_role('manager')
    print(f"Manager users: {admin_users}")