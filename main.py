from webcrawler.scrapers import LinkedInBot, GPTBot, extract_text_pdf
from users.users import Users
import os

url = "https://www.linkedin.com/jobs/search/?&f_AL=true&keywords={keyword}&origin=JOB_COLLECTION_PAGE_SEARCH_BUTTON&refresh=true"
email = "rileyjthompson5@gmail.com"
information = Users().get_information(email)


genie = GPTBot()
genie.start(mask=True)
genie.connect("https://chatgpt.com/")
genie.login()
prompt = """
    For your answer I want it you to put brackets [] around your final answer. Here is my resume: {resume} From the resume, answer the following response: create a search query on linkedin with the best chances of getting a job based on the resume
"""
resume_str = extract_text_pdf(os.getcwd()+"/users/resumes/"+information["resume_name"])
prompt = prompt.format(resume=resume_str)
genie.ask(prompt)
keyword = genie.collect_response()
print(keyword)

url = url.format(keyword=keyword)

ds = LinkedInBot()
try:
    ds.start(debug=True)
    ds.set_genie(genie)
    ds.connect(url)
    ds.login()
    ds.auto_apply(information)
    # ds.close()
except KeyboardInterrupt:
    ds.close()
except Exception as e:
    print(e)
    # ds.close()