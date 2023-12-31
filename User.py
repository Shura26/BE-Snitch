from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, prenom):
        self.id = user_id
        self.prenom = prenom

    def get_prenom(self):
        return self.prenom
    