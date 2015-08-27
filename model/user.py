import hashlib

class User:

    def __init__(self, firstName, lastName, username, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.password = password

    def addTo(self, collection):
        if collection == None:
            return False

        user = self.toJSON()
        user['password'] = hashlib.sha224(self.password).hexdigest()

        collection.insert_one(user)
        return True

    """
    Returns the current users JSON representation.
    The password field will not be added to the dictionary.
    """
    def toJSON(self):
        return {'username' : self.username, 'firstName' : self.firstName,
            'lastName' : self.lastName, 'email' : self.email}
