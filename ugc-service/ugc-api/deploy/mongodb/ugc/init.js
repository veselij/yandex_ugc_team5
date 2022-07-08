use ugc;
sh.enableSharding("ugc");
sh.shardCollection("ugc.bookmarks", {"user_id": "hashed"});
sh.shardCollection("ugc.reviews", {"movie_id": "hashed"});
sh.shardCollection("ugc.movies_likes", {"movie_id": "hashed"});
sh.shardCollection("ugc.reviews_likes", {"review_id": "hashed"});
