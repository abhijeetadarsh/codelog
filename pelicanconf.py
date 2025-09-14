AUTHOR = 'Abhijeet Adarsh'
SITENAME = 'CodeLog'
SITESUBTITLE = 'by ' + AUTHOR
SITEURL = "http://127.0.0.1:8000"

ARTICLE_PATHS = ['']
PATH = "content"
STATIC_PATHS = ['images']

TIMEZONE = 'Asia/Kolkata'
LOCALE = "C"
DEFAULT_LANG = 'en'

# Plugins
PLUGINS = ['seo']

# SEO
SEO_REPORT = True  # SEO report is enabled by default
SEO_ENHANCER = True  # SEO enhancer is disabled by default
SEO_ENHANCER_OPEN_GRAPH = True # Subfeature of SEO enhancer
SEO_ENHANCER_TWITTER_CARDS = True # Subfeature of SEO enhancer

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'themes/notmyidea'
# FAVICON = "/images/favicon.ico"

DEFAULT_PAGINATION = 6

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
GITHUB_URL =  'https://github.com/abhijeetadarsh/blog'
GITHUB_POSITION = 'right'
TWITTER_USERNAME = 'adarsh_abhijeet'

# --- Bottom Bar Customization (Theme Dependent) ---

# Some themes might allow you to add custom text here.
# For example, you might have a setting like this in your theme's configuration:
# FOOTER_TEXT = 'Content licensed under CC BY-SA 4.0'