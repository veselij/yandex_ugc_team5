from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        self.db.bookmarks.create_index([("user_id", 1), ("movie_id", 1)], unique=True)
        self.db.reviews.create_index([("movie_id", 1), ("user_id", 1)], unique=True)
        self.db.movies_likes.create_index([("movie_id", 1), ("user_id", 1)], unique=True)
        self.db.reviews_likes.create_index([("review_id", 1), ("user_id", 1)], unique=True)
