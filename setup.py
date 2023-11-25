import setuptools

VERSION = "0.0.1"

setuptools.setup(
    name="job-search",
    version=VERSION,
    description="",
    install_requires=[
        "apache_beam==2.52.0",
        "flet==0.13.0",
        "google_api_python_client==2.108.0",
        "jobspy==0.29.0",
        "protobuf==4.25.1",
        "pytest==7.4.3",
        "Requests==2.31.0",
    ],
    packages=setuptools.find_packages(),
)
