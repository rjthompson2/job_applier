from webcrawler.scrapers import LinkedInBot
from users.users import Users

url = "https://www.linkedin.com/jobs/search/?&f_AL=true&keywords={keyword}&origin=JOB_COLLECTION_PAGE_SEARCH_BUTTON&refresh=true"
email = "rileyjthompson5@gmail.com"

url = url.format(keyword="software engineer")
information = Users().get_information(email)

ds = LinkedInBot()
try:
    ds.start(debug=True)
    ds.connect(url)
    ds.login()
    ds.auto_apply(information)
    ds.close()
except:
    ds.close()