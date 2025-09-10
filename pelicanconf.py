AUTHOR = 'Abhijeet Adarsh'
SITENAME = 'blog'
SITEURL = ""

ARTICLE_PATHS = ['']
PATH = "content"
STATIC_PATHS = ['images']

TIMEZONE = 'Asia/Kolkata'
DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# THEME = 'themes/Flex'
DEFAULT_PAGINATION = 3

# --- Footer Links ---
LINKS = (
    ('About', '/pages/about.html'),
    ('Projects', '/pages/projects.html'),
    ('Contact', '/pages/contact.html'),
    ('Archives', '/archives.html'),
)

# --- Social Media Links ---
SOCIAL = (
    ('GitHub', 'https://github.com/abhijeetadarsh'),
    ('LinkedIn', 'https://linkedin.com/in/abhijeet-adarsh'),
    ('X', 'https://x.com/adarsh_abhijeet'),
)

# --- Bottom Bar Customization (Theme Dependent) ---

# Some themes might allow you to add custom text here.
# For example, you might have a setting like this in your theme's configuration:
# FOOTER_TEXT = 'Content licensed under CC BY-SA 4.0'