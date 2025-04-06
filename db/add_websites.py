import sqlite3

conn = sqlite3.connect("news_aggregator.db")
cursor = conn.cursor()

# Create the websites table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    url VARCHAR NOT NULL UNIQUE,
    topic VARCHAR NOT NULL
);
""")



conn.commit()
rss_feeds = {
    "Advertising": [
        {"name": "Adweek", "rss": "https://www.adweek.com/feed/"},
        {"name": "Marketing Week", "rss": "https://www.marketingweek.com/feed/"},
        {"name": "The Drum", "rss": "https://www.thedrum.com/rss.xml"},
        {"name": "Campaign", "rss": "https://www.campaignlive.com/rss"},
        {"name": "AdAge", "rss": "https://adage.com/rss.xml"},
        {"name": "Branding Strategy Insider", "rss": "https://www.brandingstrategyinsider.com/feed"}
    ],
    "Automotive": [
        {"name": "Autoblog", "rss": "https://www.autoblog.com/rss.xml"},
        {"name": "Car and Driver", "rss": "https://www.caranddriver.com/rss/all.xml"},
        {"name": "Auto Express", "rss": "https://www.autoexpress.co.uk/rss.xml"},
        {"name": "Jalopnik", "rss": "https://jalopnik.com/rss"},
        {"name": "Top Gear", "rss": "https://www.topgear.com/rss.xml"}
    ],
    "Biopharma": [
        {"name": "Science Magazine", "rss": "https://www.sciencemag.org/rss/news_current.xml"},
        {"name": "PharmaTimes", "rss": "https://www.pharmatimes.com/rss"},
        {"name": "BioPharma Dive", "rss": "https://www.biopharmadive.com/feeds/news/"},
        {"name": "Pharmaceutical Technology", "rss": "https://www.pharmaceutical-technology.com/feed/"},
        {"name": "Fierce Pharma", "rss": "https://www.fiercepharma.com/rss.xml"},
        {"name": "STAT News", "rss": "https://www.statnews.com/feed/"}
    ],
    "Cybersecurity": [
        {"name": "The Hacker News", "rss": "https://thehackernews.com/feeds/posts/default"},
        {"name": "Dark Reading", "rss": "https://www.darkreading.com/rss.xml"},
        {"name": "CSO Online", "rss": "https://www.csoonline.com/index.rss"},
        {"name": "Bleeping Computer", "rss": "https://www.bleepingcomputer.com/feed/"},
        {"name": "Security Week", "rss": "https://www.securityweek.com/rss"},
        {"name": "Krebs on Security", "rss": "https://krebsonsecurity.com/feed/"}
    ],
    "Energy": [
        {"name": "Renewable Energy World", "rss": "https://www.renewableenergyworld.com/rss/"},
        {"name": "Energy News Network", "rss": "https://energynews.us/feed/"},
        {"name": "Greentech Media", "rss": "https://www.greentechmedia.com/feed"},
        {"name": "OilPrice", "rss": "https://oilprice.com/rss/main"},
        {"name": "CleanTechnica", "rss": "https://cleantechnica.com/feed/"},
        {"name": "Power Technology", "rss": "https://www.power-technology.com/feed/"}
    ],
    "Financial Services": [
        {"name": "Calculated Risk", "rss": "https://www.calculatedriskblog.com/feeds/posts/default"},
        {"name": "Financial Times", "rss": "https://www.ft.com/rss/home/us"},
        {"name": "CNBC Finance", "rss": "https://www.cnbc.com/id/15839135/device/rss/rss.html"},
        {"name": "Investopedia", "rss": "https://www.investopedia.com/feedbuilder/feed"},
        {"name": "Bloomberg Markets", "rss": "https://www.bloomberg.com/markets/rss.xml"},
        {"name": "The Wall Street Journal", "rss": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"}
    ],
    "Food": [
        {"name": "Food+Tech Connect", "rss": "https://foodtechconnect.com/feed/"},
        {"name": "Serious Eats", "rss": "https://www.seriouseats.com/rss"},
        {"name": "Eater", "rss": "https://www.eater.com/rss/index.xml"},
        {"name": "Food Business News", "rss": "https://www.foodbusinessnews.net/rss"},
        {"name": "BBC Good Food", "rss": "https://www.bbcgoodfood.com/feed/rss"},
        {"name": "The Kitchn", "rss": "https://www.thekitchn.com/rss"}
    ],
    "Healthcare": [
        {"name": "Healthcare IT News", "rss": "https://www.healthcareitnews.com/rss.xml"},
        {"name": "Medical News Today", "rss": "https://www.medicalnewstoday.com/rss"},
        {"name": "Healthline", "rss": "https://www.healthline.com/rss"},
        {"name": "Science Daily - Health", "rss": "https://www.sciencedaily.com/rss/health_medicine.xml"},
        {"name": "MedPage Today", "rss": "https://www.medpagetoday.com/rss.xml"},
        {"name": "WebMD", "rss": "https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC"}
    ],
    "Industrials": [
        {"name": "Logistics Viewpoints", "rss": "https://logisticsviewpoints.com/feed/"},
        {"name": "Supply Chain Dive", "rss": "https://www.supplychaindive.com/feeds/news/"},
        {"name": "IndustryWeek", "rss": "https://www.industryweek.com/rss"},
        {"name": "The Manufacturer", "rss": "https://www.themanufacturer.com/rss"},
        {"name": "ThomasNet Industry News", "rss": "https://news.thomasnet.com/rss/all"},
        {"name": "Construction Dive", "rss": "https://www.constructiondive.com/feeds/news/"}
    ],
    
    "Media & Entertainment": [
        {"name": "Columbia Journalism Review", "rss": "https://www.cjr.org/feeds/rss.php"},
        {"name": "Variety", "rss": "https://variety.com/feed/"},
        {"name": "The Hollywood Reporter", "rss": "https://www.hollywoodreporter.com/rss"},
        {"name": "Rolling Stone", "rss": "https://www.rollingstone.com/feed/"},
        {"name": "IndieWire", "rss": "https://www.indiewire.com/feed/"},
        {"name": "Deadline", "rss": "https://deadline.com/feed/"},
        {"name": "Billboard", "rss": "https://www.billboard.com/rss"},
        {"name": "The Wrap", "rss": "https://www.thewrap.com/feed/"},
        {"name": "Screen Rant", "rss": "https://screenrant.com/feed/"},
        {"name": "CNET Entertainment", "rss": "https://www.cnet.com/rss/news/"},
        {"name": "IGN Entertainment", "rss": "https://www.ign.com/articles/feed"},
        {"name": "NME", "rss": "https://www.nme.com/rss"}
    ],
        "Medical Devices": [
        {"name": "Science Magazine - Medical Devices", "rss": "https://www.science.org/action/showFeed?type=etoc&feed=rss&jc=sci"},
        {"name": "MedTech Dive", "rss": "https://www.medtechdive.com/rss"},
        {"name": "MD+DI Online", "rss": "https://www.mddionline.com/rss.xml"},
        {"name": "Medical Device Network", "rss": "https://www.medicaldevice-network.com/feed/"},
        {"name": "MassDevice", "rss": "https://www.massdevice.com/feed/"},
        {"name": "MedPage Today", "rss": "https://www.medpagetoday.com/rss.cfm"},
    ],
    "Real Estate": [
        {"name": "Inman", "rss": "https://www.inman.com/feed/"},
        {"name": "HousingWire", "rss": "https://www.housingwire.com/rss"},
        {"name": "Realtor Magazine", "rss": "https://realtormag.realtor.org/rss.xml"},
        {"name": "The Real Deal", "rss": "https://therealdeal.com/feed/"},
        {"name": "CRETech", "rss": "https://www.cretech.com/feed/"},
        {"name": "PropertyWire", "rss": "https://www.propertywire.com/feed/"},
    ],
    "Retail": [
        {"name": "Refinery29", "rss": "https://www.refinery29.com/rss.xml"},
        {"name": "Retail Dive", "rss": "https://www.retaildive.com/rss"},
        {"name": "Retail Wire", "rss": "https://www.retailwire.com/feed/"},
        {"name": "Chain Store Age", "rss": "https://www.chainstoreage.com/rss"},
        {"name": "National Retail Federation", "rss": "https://nrf.com/rss.xml"},
        {"name": "eMarketer Retail", "rss": "https://www.emarketer.com/Rss.aspx?section=Retail"},
    ],
    "Telecom": [
        {"name": "Light Reading", "rss": "https://www.lightreading.com/rss_simple.asp"},
        {"name": "Telecoms.com", "rss": "https://telecoms.com/feed/"},
        {"name": "RCR Wireless News", "rss": "https://www.rcrwireless.com/feed"},
        {"name": "Fierce Telecom", "rss": "https://www.fiercetelecom.com/rss/xml"},
        {"name": "Total Telecom", "rss": "https://www.totaltele.com/rss/tt_news.xml"},
        {"name": "Telecom Review", "rss": "https://www.telecomreview.com/index.php/rss-news"},
    ],
    "Travel & Hospitality": [
        {"name": "Skift", "rss": "https://skift.com/feed/"},
        {"name": "Travel Weekly", "rss": "https://www.travelweekly.com/rss/"},
        {"name": "Lonely Planet", "rss": "https://www.lonelyplanet.com/news/rss"},
        {"name": "Hospitality Net", "rss": "https://www.hospitalitynet.org/feed.rss"},
        {"name": "Travel Pulse", "rss": "https://www.travelpulse.com/rss"},
        {"name": "The Points Guy", "rss": "https://thepointsguy.com/feed/"},
    ],
        "Cryptocurrency": [
        {"name": "CoinDesk", "rss": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
        {"name": "CoinTelegraph", "rss": "https://cointelegraph.com/rss"},
        {"name": "Bitcoin Magazine", "rss": "https://bitcoinmagazine.com/.rss/full/"},
        {"name": "Decrypt", "rss": "https://decrypt.co/feed"},
        {"name": "CryptoSlate", "rss": "https://cryptoslate.com/feed/"},
        {"name": "The Block", "rss": "https://www.theblock.co/rss"},
    ],
    "Mixed Reality": [
        {"name": "Road to VR", "rss": "https://www.roadtovr.com/feed/"},
        {"name": "UploadVR", "rss": "https://uploadvr.com/feed/"},
        {"name": "VRScout", "rss": "https://vrscout.com/feed/"},
        {"name": "AR Post", "rss": "https://arpost.co/feed/"},
        {"name": "XR Today", "rss": "https://www.xrtoday.com/feed/"},
        {"name": "VRFocus", "rss": "https://www.vrfocus.com/feed/"},
    ],
    "Internet of Things": [
        {"name": "IoT Business News", "rss": "https://iotbusinessnews.com/feed/"},
        {"name": "IoT For All", "rss": "https://www.iotforall.com/feed"},
        {"name": "Postscapes IoT", "rss": "https://www.postscapes.com/feed/"},
        {"name": "IoT Now", "rss": "https://www.iot-now.com/feed/"},
        {"name": "Hackster.io IoT", "rss": "https://www.hackster.io/rss.xml"},
        {"name": "Network World IoT", "rss": "https://www.networkworld.com/category/internet-of-things/index.rss"},
    ],
    "Machine Learning": [
        {"name": "ScienceDaily - Artificial Intelligence", "rss": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml"},
        {"name": "MIT News - AI", "rss": "http://news.mit.edu/rss/topic/artificial-intelligence"},
        {"name": "Google AI Blog", "rss": "https://ai.googleblog.com/feeds/posts/default"},
        {"name": "OpenAI Blog", "rss": "https://openai.com/research/feed.xml"},
        {"name": "Towards Data Science", "rss": "https://towardsdatascience.com/feed"},
        {"name": "DeepMind Blog", "rss": "https://www.deepmind.com/blog/rss.xml"},
    ],
    "Entrepreneurship": [
        {"name": "Entrepreneur", "rss": "https://www.entrepreneur.com/feed"},
        {"name": "Harvard Business Review", "rss": "https://hbr.org/feed"},
        {"name": "Startup Grind", "rss": "https://www.startupgrind.com/feed/"},
        {"name": "Seth Godin’s Blog", "rss": "https://seths.blog/feed/"},
        {"name": "TechCrunch Startups", "rss": "https://techcrunch.com/startups/feed/"},
        {"name": "Inc. Magazine", "rss": "https://www.inc.com/rss"},
    ],
    "Leadership": [
        {"name": "Leading Blog", "rss": "https://www.leadershipnow.com/blog/rss.xml"},
        {"name": "Michael Hyatt", "rss": "https://fullfocus.co/blog/feed/"},
        {"name": "Leadership Freak", "rss": "https://leadershipfreak.blog/feed/"},
        {"name": "Harvard Business Review - Leadership", "rss": "https://hbr.org/topic/leadership/feed"},
        {"name": "Forbes Leadership", "rss": "https://www.forbes.com/leadership/feed/"},
        {"name": "John Maxwell Blog", "rss": "https://www.johnmaxwell.com/blog/feed/"},
    ],
    "Economics": [
        {"name": "Greg Mankiw's Blog", "rss": "https://gregmankiw.blogspot.com/feeds/posts/default"},
        {"name": "The Economist", "rss": "https://www.economist.com/finance-and-economics/rss.xml"},
        {"name": "Freakonomics", "rss": "https://freakonomics.com/feed/"},
        {"name": "Marginal Revolution", "rss": "https://marginalrevolution.com/feed"},
        {"name": "Naked Capitalism", "rss": "https://www.nakedcapitalism.com/feed"},
        {"name": "VoxEU Economics", "rss": "https://voxeu.org/rss.xml"},
    ],
    "Programming": [
        {"name": "Martin Fowler", "rss": "https://martinfowler.com/feed.atom"},
        {"name": "Hacker News", "rss": "https://news.ycombinator.com/rss"},
        {"name": "Dev.to", "rss": "https://dev.to/feed"},
        {"name": "Smashing Magazine", "rss": "https://www.smashingmagazine.com/feed/"},
        {"name": "CSS-Tricks", "rss": "https://css-tricks.com/feed/"},
        {"name": "Reddit Programming", "rss": "https://www.reddit.com/r/programming/.rss"},
    ],
    "SEO": [
        {"name": "Moz Blog", "rss": "https://moz.com/blog/feed"},
        {"name": "Search Engine Journal", "rss": "https://www.searchenginejournal.com/feed/"},
        {"name": "Search Engine Land", "rss": "https://feeds.searchengineland.com/"},
        {"name": "Neil Patel Blog", "rss": "https://neilpatel.com/blog/feed/"},
        {"name": "Backlinko", "rss": "https://backlinko.com/feed"},
        {"name": "Ahrefs Blog", "rss": "https://ahrefs.com/blog/feed/"},
    ],
    "Management": [
        {"name": "Management Issues", "rss": "https://www.management-issues.com/rss"},
        {"name": "Harvard Business Review - Management", "rss": "https://hbr.org/topic/management/feed"},
        {"name": "Sloan Management Review", "rss": "https://sloanreview.mit.edu/feed/"},
        {"name": "Forbes Management", "rss": "https://www.forbes.com/management/feed/"},
        {"name": "McKinsey & Company", "rss": "https://www.mckinsey.com/rss"},
        {"name": "Strategy+Business", "rss": "https://www.strategy-business.com/rss"},
    ],
    "Photography": [
        {"name": "Digital Photography School", "rss": "https://digital-photography-school.com/feed/"},
        {"name": "PetaPixel", "rss": "https://petapixel.com/feed/"},
        {"name": "Fstoppers", "rss": "https://fstoppers.com/feed"},
        {"name": "DPReview", "rss": "https://www.dpreview.com/feeds/news"},
        {"name": "DIY Photography", "rss": "https://www.diyphotography.net/feed/"},
        {"name": "Photography Life", "rss": "https://photographylife.com/feed"},
    ],
    "Data Science": [
        {"name": "KDnuggets", "rss": "https://www.kdnuggets.com/feed"},
        {"name": "Towards Data Science", "rss": "https://towardsdatascience.com/feed"},
        {"name": "Data Science Central", "rss": "https://www.datasciencecentral.com/profiles/blog/feed"},
        {"name": "Analytics Vidhya", "rss": "https://www.analyticsvidhya.com/feed/"},
        {"name": "R Bloggers", "rss": "https://www.r-bloggers.com/feed/"},
        {"name": "Machine Learning Mastery", "rss": "https://machinelearningmastery.com/blog/feed/"},
    ],
    "Writing": [
        {"name": "ProWritingAid", "rss": "https://prowritingaid.com/en/Blog/rss"},
        {"name": "The Write Life", "rss": "https://thewritelife.com/feed/"},
        {"name": "Writing Cooperative", "rss": "https://writingcooperative.com/feed"},
        {"name": "Jane Friedman Blog", "rss": "https://www.janefriedman.com/feed/"},
        {"name": "Copyblogger", "rss": "https://copyblogger.com/feed/"},
        {"name": "Writer's Digest", "rss": "https://www.writersdigest.com/.rss/full/"},
    ],
    "Creativity": [
        {"name": "99U", "rss": "https://99u.adobe.com/feed"},
        {"name": "Creative Boom", "rss": "https://www.creativeboom.com/feed/"},
        {"name": "The Creativity Post", "rss": "https://www.creativitypost.com/rss"},
        {"name": "IDEO Blog", "rss": "https://www.ideo.com/blog/feed"},
        {"name": "Creative Review", "rss": "https://www.creativereview.co.uk/feed/"},
        {"name": "Design Observer", "rss": "https://designobserver.com/feeds/rss.xml"},
    ],
    "Content Marketing": [
        {"name": "Content Marketing Institute", "rss": "https://contentmarketinginstitute.com/feed/"},
        {"name": "Copyblogger", "rss": "https://copyblogger.com/feed/"},
        {"name": "Neil Patel Blog", "rss": "https://neilpatel.com/blog/feed/"},
        {"name": "HubSpot Blog", "rss": "https://blog.hubspot.com/marketing/rss.xml"},
        {"name": "MarketingProfs", "rss": "https://www.marketingprofs.com/rss/"},
        {"name": "Search Engine Journal - Content Marketing", "rss": "https://www.searchenginejournal.com/category/content-marketing/feed/"},
    ],
    "Marketing": [
        {"name": "MarketingProfs", "rss": "https://www.marketingprofs.com/rss/"},
        {"name": "HubSpot Blog", "rss": "https://blog.hubspot.com/marketing/rss.xml"},
        {"name": "Moz Blog", "rss": "https://moz.com/blog/feed"},
        {"name": "Social Media Examiner", "rss": "https://www.socialmediaexaminer.com/feed/"},
        {"name": "Search Engine Land", "rss": "https://feeds.searchengineland.com/"},
        {"name": "Neil Patel Blog", "rss": "https://neilpatel.com/blog/feed/"},
    ],
    "Comics": [
        {"name": "xkcd", "rss": "https://xkcd.com/rss.xml"},
        {"name": "The Oatmeal", "rss": "https://theoatmeal.com/blog/feed/rss"},
        {"name": "Saturday Morning Breakfast Cereal", "rss": "https://www.smbc-comics.com/rss.php"},
        {"name": "Questionable Content", "rss": "https://www.questionablecontent.net/QCRSS.xml"},
        {"name": "Dilbert", "rss": "https://dilbert.com/feed"},
    ],
    "Gaming": [
        {"name": "Kotaku", "rss": "https://kotaku.com/rss"},
        {"name": "IGN", "rss": "https://feeds.ign.com/ign/all"},
        {"name": "Polygon", "rss": "https://www.polygon.com/rss/index.xml"},
        {"name": "Game Informer", "rss": "https://www.gameinformer.com/rss.xml"},
        {"name": "PC Gamer", "rss": "https://www.pcgamer.com/rss/"},
    ],
    "Food": [
        {"name": "Smitten Kitchen", "rss": "https://smittenkitchen.com/feed/"},
        {"name": "Serious Eats", "rss": "https://www.seriouseats.com/rss"},
        {"name": "Food52", "rss": "https://food52.com/blog/feed"},
        {"name": "Simply Recipes", "rss": "https://www.simplyrecipes.com/feed"},
        {"name": "The Kitchn", "rss": "https://www.thekitchn.com/rss"},
    ],
    "Travel": [
        {"name": "The Points Guy", "rss": "https://thepointsguy.com/feed/"},
        {"name": "Nomadic Matt", "rss": "https://www.nomadicmatt.com/feed/"},
        {"name": "Lonely Planet", "rss": "https://www.lonelyplanet.com/blog.rss"},
        {"name": "Wanderlust", "rss": "https://www.wanderlust.co.uk/rss/"},
        {"name": "Roads & Kingdoms", "rss": "https://roadsandkingdoms.com/feed/"},
    ],
    "Music": [
        {"name": "Stereogum", "rss": "https://www.stereogum.com/feed/"},
        {"name": "Pitchfork", "rss": "https://pitchfork.com/rss/news/"},
        {"name": "Rolling Stone Music", "rss": "https://www.rollingstone.com/music/music-news/feed/"},
        {"name": "NPR Music", "rss": "https://www.npr.org/rss/rss.php?id=1039"},
        {"name": "Consequence", "rss": "https://consequence.net/feed/"},
    ],
    "Culture": [
        {"name": "Boing Boing", "rss": "https://boingboing.net/feed"},
        {"name": "Brain Pickings", "rss": "https://www.brainpickings.org/feed/"},
        {"name": "Open Culture", "rss": "https://www.openculture.com/rss"},
        {"name": "Aeon", "rss": "https://aeon.co/feed"},
        {"name": "The Atlantic - Culture", "rss": "https://feeds.theatlantic.com/atlantic/culture"},
    ],
    "Crafts": [
        {"name": "Make: DIY Projects", "rss": "https://makezine.com/feed/"},
        {"name": "Craft Gossip", "rss": "https://craftgossip.com/feed/"},
        {"name": "Crafts by Amanda", "rss": "https://craftsbyamanda.com/feed/"},
        {"name": "DIY & Crafts", "rss": "https://www.diyncrafts.com/feed"},
        {"name": "CraftGawker", "rss": "https://www.craftgawker.com/rss"},
    ],
    "Dating": [
        {"name": "New York Times - Modern Love", "rss": "https://www.nytimes.com/column/modern-love/rss.xml"},
        {"name": "The Love Life", "rss": "https://www.thelovelife.com/feed/"},
        {"name": "Dating Advice", "rss": "https://www.datingadvice.com/feed"},
        {"name": "Psychology Today - Dating", "rss": "https://www.psychologytoday.com/us/blog/dating-and-mating/feed"},
        {"name": "Zoosk Blog", "rss": "https://www.zoosk.com/date-mix/feed/"},
    ]


}

# # Insert RSS feeds into the database
# i=0
# for topic, feeds in rss_feeds.items():
#     for feed in feeds:
#         cursor.execute(
#             "INSERT OR IGNORE INTO websites (id, name, url, topic) VALUES (?,?, ?, ?)",
#             (i+1,feed["name"], feed["rss"], topic)
#         )
#         i+=1

conn.commit()
news_websites = [
    {"name": "BBC News", "url": "http://feeds.bbci.co.uk/news/rss.xml", "topic": "World"},
    {"name": "CNN Top Stories", "url": "http://rss.cnn.com/rss/edition.rss", "topic": "World"},
    {"name": "Reuters Top News", "url": "http://feeds.reuters.com/reuters/topNews", "topic": "Business"},
    {"name": "Al Jazeera", "url": "http://www.aljazeera.com/xml/rss/all.xml", "topic": "Middle East"},
    {"name": "The Guardian World", "url": "https://www.theguardian.com/world/rss", "topic": "World"},
    {"name": "NY Times Home", "url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml", "topic": "World"},
    {"name": "Fox News", "url": "http://feeds.foxnews.com/foxnews/latest", "topic": "Politics"},
    {"name": "NBC News", "url": "http://feeds.nbcnews.com/nbcnews/public/news", "topic": "US"},
    {"name": "CBS News", "url": "http://feeds.cbsnews.com/rss/cbsnews_latest", "topic": "US"},
    {"name": "Bloomberg", "url": "https://www.bloomberg.com/feed/podcast/etf-report.xml", "topic": "Business"},
    {"name": "Financial Times", "url": "http://www.ft.com/rss/home/us", "topic": "Business"},
    {"name": "Forbes", "url": "https://www.forbes.com/investing/feed/", "topic": "Business"},
    {"name": "TechCrunch", "url": "http://feeds.feedburner.com/TechCrunch/", "topic": "Technology"},
    {"name": "Wired", "url": "https://www.wired.com/feed/category/gear/latest/rss", "topic": "Technology"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "topic": "Technology"},
    {"name": "CNET", "url": "https://www.cnet.com/rss/all/", "topic": "Technology"},
    {"name": "Vox", "url": "https://www.vox.com/rss/index.xml", "topic": "Politics"},
    {"name": "HuffPost", "url": "https://www.huffpost.com/section/front-page/feed", "topic": "Politics"},
    {"name": "USA Today", "url": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories", "topic": "US"},
    {"name": "Los Angeles Times", "url": "https://www.latimes.com/rss2.0.xml", "topic": "US"},
    {"name": "Wall Street Journal", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml", "topic": "Business"},
    {"name": "Newsweek", "url": "https://www.newsweek.com/rss", "topic": "Politics"},
    {"name": "Time", "url": "http://feeds.feedburner.com/time/topstories", "topic": "Politics"},
    {"name": "BuzzFeed News", "url": "https://www.buzzfeed.com/world.xml", "topic": "Entertainment"},
    {"name": "Vice News", "url": "https://www.vice.com/en_us/rss", "topic": "World"},
    {"name": "Politico", "url": "https://www.politico.com/rss/politicopicks.xml", "topic": "Politics"},
    {"name": "The Hill", "url": "https://thehill.com/rss/syndicator/19109", "topic": "Politics"},
    {"name": "Business Insider", "url": "https://www.businessinsider.com/rss", "topic": "Business"},
    {"name": "CNBC", "url": "https://www.cnbc.com/id/10000664/device/rss/rss.html", "topic": "Business"},
    {"name": "ESPN", "url": "https://www.espn.com/espn/rss/news", "topic": "Sports"},
    {"name": "Sports Illustrated", "url": "https://www.si.com/rss/si_topstories.rss", "topic": "Sports"},
    {"name": "Sky Sports", "url": "https://www.skysports.com/rss/12040", "topic": "Sports"},
    {"name": "Eurosport", "url": "https://www.eurosport.com/rss.xml", "topic": "Sports"},
    {"name": "TechRadar", "url": "https://www.techradar.com/rss", "topic": "Technology"},
    {"name": "ZDNet", "url": "https://www.zdnet.com/news/rss.xml", "topic": "Technology"},
    {"name": "Gizmodo", "url": "https://gizmodo.com/rss", "topic": "Technology"},
    {"name": "Mashable", "url": "http://feeds.mashable.com/Mashable", "topic": "Entertainment"},
    {"name": "Digital Trends", "url": "https://www.digitaltrends.com/feed/", "topic": "Technology"},
    {"name": "PCMag", "url": "https://www.pcmag.com/rss/news", "topic": "Technology"},
    {"name": "Scientific American", "url": "https://www.scientificamerican.com/feed/rss/", "topic": "Science"},
    {"name": "National Geographic", "url": "https://www.nationalgeographic.com/content/natgeo/en_us/rss", "topic": "Science"},
    {"name": "New Scientist", "url": "https://www.newscientist.com/feed/home/", "topic": "Science"},
    {"name": "Nature", "url": "http://feeds.nature.com/nature/rss/current", "topic": "Science"},
    {"name": "Medical News Today", "url": "https://www.medicalnewstoday.com/rss", "topic": "Health"},
    {"name": "WebMD", "url": "https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC", "topic": "Health"},
    {"name": "Healthline", "url": "https://www.healthline.com/rss", "topic": "Health"},
    {"name": "Men's Health", "url": "https://www.menshealth.com/rss/all.xml", "topic": "Health"},
    {"name": "Women's Health", "url": "https://www.womenshealthmag.com/rss", "topic": "Health"},
    {"name": "Travel + Leisure", "url": "https://www.travelandleisure.com/rss", "topic": "Travel"},
    {"name": "Lonely Planet", "url": "https://www.lonelyplanet.com/rss", "topic": "Travel"},
    {"name": "Condé Nast Traveler", "url": "https://www.cntraveler.com/rss", "topic": "Travel"},
    {"name": "Eater", "url": "https://www.eater.com/rss/index.xml", "topic": "Food"},
    {"name": "Bon Appétit", "url": "https://www.bonappetit.com/feed/rss", "topic": "Food"},
    {"name": "Food Network", "url": "http://www.foodnetwork.com/rss", "topic": "Food"},
    {"name": "Delish", "url": "https://www.delish.com/rss/all/", "topic": "Food"},
    {"name": "Serious Eats", "url": "https://www.seriouseats.com/rss", "topic": "Food"},
    {"name": "The Daily Meal", "url": "https://www.thedailymeal.com/rss", "topic": "Food"},
    {"name": "Quartz", "url": "https://qz.com/feed/", "topic": "Business"},
    {"name": "Axios", "url": "https://api.axios.com/feed/", "topic": "Politics"},
    {"name": "Vulture", "url": "https://www.vulture.com/rss/index.xml", "topic": "Entertainment"},
    {"name": "Rolling Stone", "url": "https://www.rollingstone.com/feed", "topic": "Entertainment"},
    {"name": "NME", "url": "https://www.nme.com/rss", "topic": "Entertainment"},
    {"name": "Billboard", "url": "https://www.billboard.com/feed", "topic": "Entertainment"},
    {"name": "Variety", "url": "https://variety.com/feed/", "topic": "Entertainment"},
    {"name": "Deadline", "url": "https://deadline.com/feed/", "topic": "Entertainment"},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/t/feed", "topic": "Entertainment"},
    {"name": "The Wrap", "url": "https://www.thewrap.com/feed/", "topic": "Entertainment"},
    {"name": "Entertainment Weekly", "url": "https://ew.com/feed/", "topic": "Entertainment"},
    {"name": "MTV News", "url": "http://www.mtv.com/news/rss", "topic": "Entertainment"},
    {"name": "Complex", "url": "https://www.complex.com/rss", "topic": "Entertainment"},
    {"name": "Pitchfork", "url": "https://pitchfork.com/rss/news/", "topic": "Entertainment"},
    {"name": "Stereogum", "url": "https://www.stereogum.com/feed/", "topic": "Entertainment"},
    {"name": "TechNode", "url": "https://technode.com/feed/", "topic": "Technology"},
    {"name": "VCCircle", "url": "https://www.vccircle.com/feed/", "topic": "Business"},
    {"name": "The Economic Times", "url": "https://economictimes.indiatimes.com/rssfeedsdefault.cms", "topic": "Business"},
    {"name": "NDTV", "url": "https://feeds.feedburner.com/ndtvnews-india-news", "topic": "India"},
    {"name": "India Today", "url": "https://www.indiatoday.in/rss", "topic": "India"},
    {"name": "The Hindu", "url": "https://www.thehindu.com/feeder/default.rss", "topic": "India"},
    {"name": "Hindustan Times", "url": "https://www.hindustantimes.com/rss", "topic": "India"},
    {"name": "Deccan Herald", "url": "https://www.deccanherald.com/rss", "topic": "India"}
]

print("Total websites to insert:", len(news_websites))

# Connect to the SQLite database (assumes news_aggregator.db is in the current directory)

# Create the websites table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    url VARCHAR NOT NULL UNIQUE,
    topic VARCHAR NOT NULL
);
""")
site = {"name": "ESPN", "url": "https://www.espn.com/espn/rss/news", "topic": "Sports"}
# Insert each website into the table with a unique ID
# for _, site in enumerate(news_websites):
#     cursor.execute(
#         "INSERT OR IGNORE INTO websites (id, name, url, topic) VALUES (?, ?, ?, ?)",
#         (i + 1, site["name"], site["url"], site["topic"])
#     )
#     i+=1
cursor.execute(
    "INSERT OR IGNORE INTO websites (id, name, url, topic) VALUES (?, ?, ?, ?)",
    (305, site["name"], site["url"], site["topic"])
)

conn.commit()
conn.close()


print("Inserted", len(news_websites), "website sources into the websites table.")
