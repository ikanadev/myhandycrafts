"""StorePost model."""

# Django
from django.db import models

#utils
from myhandycrafts.utils.models import MyHandycraftsModel

class StorePost(MyHandycraftsModel):
    """ StorePost model.

    Save the relationship betwen post on store.
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
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        verbose_name='stores'
    )

    def __str__(self):
        return "{} {} {}".format(
            str(self.post.user),
            str(self.post),
            str(self.store)
        )

