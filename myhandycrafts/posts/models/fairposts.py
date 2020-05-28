"""FairPost model."""

# Django
from django.db import models

#utils
from myhandycrafts.utils.models import MyHandycraftsModel

class FairPost(MyHandycraftsModel):
    """ FairPost model.

    Save the relationship betwen post on fair.
    """
    user = models.ForeignKey('users.User',
                             on_delete=models.CASCADE,
                             verbose_name='users'
                             )

    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        verbose_name='posts',
    )
    fair = models.ForeignKey(
        'fairs.Fair',
        on_delete=models.CASCADE,
        verbose_name='fairs'
    )

    def __str__(self):
        return "{} {} {}".format(
            str(self.post.user),
            str(self.post),
            str(self.fair)
        )
