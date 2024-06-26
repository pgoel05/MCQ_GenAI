from setuptools import find_packages, setup

setup(
    name="mcq_generator",
    version="0.0.1",
    author="Prateek Goel",
    install_requires=[
        "langchain",
        "pandas",
        "PyPDF2",
        "openai",
        "streamlit",
        "python-dotenv",
    ],
    packages=find_packages(),
)
