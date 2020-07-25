Scraping courses as no API from the university for courses (uni not giving access to DB). Cannot be headless Selenium or Beautiful Soup as public course guide doesn't have sorting options and private course guide needs sign in with 2fa (2fa cookies exp req make it difficult to ask user cookies).

Speed bottlenecks: selenium course gathering (GUI load speed), course check database (DB is slow) - mostly code external although may be able to build workarounds if needed
