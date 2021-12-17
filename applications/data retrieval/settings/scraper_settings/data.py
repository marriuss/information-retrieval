URL = "https://heroesportal.net/"

PARSED_URL_PATTERNS = {
        "article": r"https?://heroesportal\.net/library/index\.php\?version=([\w\d]{2,3})&page=(\w+)$",
        "active_clan": r"https?://heroesportal\.net/clans\.php\?id=(\d+)$",
        "disabled_clan": r"https?://heroesportal\.net/archive/clans/(\d+)$",
        "map": r"https?://heroesportal\.net/maps/view/(\d+)$",
        "profile": r"https?://heroesportal\.net/profile\.php\?id=(\d+)$",
}

IGNORED_URL_PATTERNS = [
        r"https?://heroesportal\.net/maps/view/(\d+)#(.+)",
        r"https?://heroesportal\.net/library/index\.php\?version=([\w\d]{2,3})&page=(\w+)#(.+)",
        r"https?://heroesportal\.net/partners",
        r"https?://heroesportal\.net/maps/download",
        r"https?://heroesportal\.net/maps/view/(\d+)/p(\d+)",
        r"https?://heroesportal\.net/maps/user",
        r"https?://heroesportal\.net/tavern",
        r"https?://heroesportal\.net/barstand",
        r"https?://heroesportal\.net/archive/magisters",
        r"https?://heroesportal\.net/user",
        r"https?://heroesportal\.net/faq",
        r"https?://heroesportal\.net/stats",
        r"https?://heroesportal\.net/events",
        r"https?://heroesportal\.net/votearchive",
        r"https?://heroesportal\.net/rss",
        r"https?://heroesportal\.net/land",
        r"https?://heroesportal\.net/refill",
        r"https?://heroesportal\.net/newspaper",
        r"https?://heroesportal\.net/newsarchive",
        r"https?://heroesportal\.net/getfile",
        r"https?://heroesportal\.net/shop",
        r"https?://heroesportal\.net/files",
        r"https?://heroesportal\.net/library/school",
        r"https?://heroesportal\.net/other",
        r"https?://heroesportal\.net(.*)lang=english",
        r"https?://heroesportal\.net(.*)lang=russian",
        r"https?://www\.liveinternet\.ru/click",
]
