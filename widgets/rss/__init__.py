from .rss import main

default = '''# Store your list of feeds as key-value pairs here:
[rss.feeds]
"Hacker News" = "https://news.ycombinator.com/rss"

# Subfolders are defined like this:
[rss.feeds.Subfolder]
"Lobste.rs" = "https://lobste.rs/rss"'''