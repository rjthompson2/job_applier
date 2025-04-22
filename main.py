from webcrawler.navigate import DynamicScraper
from users.users import Users

url = "https://www.linkedin.com/jobs/search/?&f_AL=true&keywords=software%20engineer&origin=JOB_COLLECTION_PAGE_SEARCH_BUTTON&refresh=true"
email = "rileyjthompson5@gmail.com"

information = Users().get_information(email)

ds = DynamicScraper()
ds.start(debug=True)
ds.connect(url)
ds.login()
ds.auto_apply(information)
# values = ds.collect()
# print(values)