from django.db import models

# The Assignment says:

# A "Thread" consists of the following:
# A title field (simple varchar field, required)
# A username field (simple varchar field, required)
# A description field comment (simple varchar field, optional)
# A list of child Comments
# Clicking a Thread should bring up the "Thread Detail View"
# The Thread Detail View should show the Thread's child Comments and a form to (anonymously) submit a new Comment

# A "Comment" consists of the following:
# A text field (simple varchar field, required)
# A username field (simple varchar field, required)
# A score field (integer, this should not be included in the Comment form but users should be able to modify the score by upvoting or downvoting an existing Comment)

# Thread model
class Thread(models.Model):
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    # optional field
    description = models.CharField(max_length=200, null=True)

# Comment model
class Comment(models.Model):
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    score = models.IntegerField(default=0)
