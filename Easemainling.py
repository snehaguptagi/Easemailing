import praw
from typing import List, Dict
import os

class BrowserTool:
    def scrape_reddit(self, max_comments_per_post: int = 7) -> List[Dict]:
        """
        Scrape Reddit content from the LocalLLAMA subreddit.

        Args:
            max_comments_per_post (int): Maximum number of comments to load per post.

        Returns:
            List[Dict]: A list of dictionaries containing the post title, URL, and comments.
        """
        try:
            # Initialize the Reddit client
            reddit = praw.Reddit(
                client_id=os.environ["REDDIT_CLIENT_ID"],
                client_secret=os.environ["REDDIT_CLIENT_SECRET"],
                user_agent=os.environ["REDDIT_USER_AGENT"],
            )

            # Define the subreddit to scrape
            subreddit = reddit.subreddit("LocalLLAMA")
            scraped_data = []

            # Iterate over the top posts
            for post in subreddit.hot(limit=12):
                post_data = {"title": post.title, "url": post.url, "comments": []}

                # Load the comments in batches
                comments = post.comments.list()
                for comment in comments[:max_comments_per_post]:
                    post_data["comments"].append(comment.body)

                scraped_data.append(post_data)

            return scraped_data
        except praw.exceptions.ClientException as e:
            print(f"Error: {e}")
            return []