from setuptools import setup, find_packages
from typing import List
HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

    
setup(
    name='myntra-review-scrapper',
    version= '0.0.1',
    author='Daizy',
    author_email='daizy@gmail.com',
    description='End-to-end web scraping pipeline for extracting, processing, and visualizing Myntra product reviews using Selenium, BeautifulSoup, and Streamlit',
    url='https://github.com/DAIZYGUPTA/myntra-review-scrapper',
    install_requires= get_requirements('requirements.txt'),
    packages=find_packages()
)
