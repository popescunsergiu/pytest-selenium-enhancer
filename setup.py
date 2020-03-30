from setuptools import setup

setup(
    name="pytest-selenium-enhancer",
    use_scm_version=True,
    description="pytest plugin for Selenium",
    long_description=open("README.rst").read(),
    author="Sergiu Popescu",
    author_email="popescunsergiu@gmail.com",
    url="https://github.com/popescunsergiu/pytest-selenium-enhancer",
    packages=["pytest_selenium_enhancer"],
    install_requires=[
        "numpy",
        "opencv-python>=4.2.0.32",
        "Pillow>=7.0.0",
        "pylint>=2.4.4",
        "pytest>=5.3.0",
        "pytest-variables>=1.9.0",
        "requests",
        "selenium>=3.141.0"
    ],
    entry_points={
        "pytest11": ["pytest-selenium-enhancer = pytest_selenium_enhancer.plugin"]
    },
    setup_requires=["setuptools_scm"],
    license="MIT License",
    keywords="py.test pytest qa",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)