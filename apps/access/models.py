from django.db import models


class InvitedEmail(models.Model):
    """
    A model that maintains a list of invited email addresses
    for the purposes of allowing Google authentication and signup.

    Effectively, an email must appear in an instance of this model
    in order to sign up, which is required to be able to log in.

    Removing an instance will effectively block a user from login, but
    it is advised to disable the user's auth.User entry as well.
    """

    address = models.EmailField(unique=True)

    def __str__(self):
        return self.address
