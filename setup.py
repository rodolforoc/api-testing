from setuptools import setup, find_packages

setup(name='api-testing-framework',
      version='1.0',
      description="Practice API Testing",
      author='Rodolfo Caetano',
      author_email='rodolforoc97@gmail.com',
      url='',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
            "pytest",
            "pytest-html",
            "requests",
            "requests-oauthlib",
            "PyMySQL",
            "WooCommerce",
      ]
      )