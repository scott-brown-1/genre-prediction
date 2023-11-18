from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    reqs = f.read().splitlines()

setup(
    name='spotifyapi',
    version='0.0.1',
    packages=find_packages(),
    description='Spotify API wrapper',
    author='Jake Anderson, Scott Brown',
    author_email='jakejoeanderson@gmail.com,scottdbrown7@gmail.com',
    url = 'githup.com',
    install_requires = reqs,
    long_description=readme,
    long_description_content_type='text/markdown',
)