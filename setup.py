from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name="mypackage",
            maintainer="jdbohrman",
            maintainer_email="",
            description="Encourage, track & analyze personal growth.",
            long_description="Encourage, track & analyze personal growth.",
            url="https://github.com/jonhue/the_growth_app",
            download_url="https://github.com/jonhue/the_growth_app",
            license="MIT",
            packages=PACKAGES)


if __name__ == '__main__':
    setup(**opts)