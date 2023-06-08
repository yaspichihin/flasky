# Add db session
from manage import app, db

# Add models
from app.models import Role, User


def add_test_data():
    # Add roles
    admin = Role(name="admin")
    moderator = Role(name="moderator")
    user = Role(name="user")

    # Add users
    john = User(username="john", role=admin)
    susan = User(username="susan", role=moderator)
    david = User(username="david", role=user)
    ivan = User(username="ivan", role=user)
    stas = User(username="stas", role=user)
    petr = User(username="petr", role=user)

    db.session.add_all(
        [
            admin,
            moderator,
            user,

            john,
            susan,
            david,
            ivan,
            stas,
            petr,
        ]
    )


if __name__ == "__main__":
    with app.app_context():
        add_test_data()
