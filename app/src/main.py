
import os

from dotenv import load_dotenv

from scrappers.pvue_login import login_to_website
from scrappers.scrape_grades import process_grades
from scrappers.scrape_assignments import process_assignments

# Load environment variables
load_dotenv(verbose=True)



def main():

    url = os.getenv("PVUE_URL")
    user = os.getenv("PVUE_USERNAME")
    pwd = os.getenv("PVUE_PASS")

    s_driver = None

    try:
        data_output_format = os.environ.get("DATA_OUTPUT_FORMAT")

        s_driver = login_to_website(url,user,pwd)
        #process_grades(s_driver, data_output_format)
        process_assignments(s_driver, data_output_format)

    except Exception as e:
        print(e)
    finally:
        if s_driver:
            s_driver.quit()


if __name__ == "__main__":
    main()
