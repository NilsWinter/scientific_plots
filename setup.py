try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

__version__ = '0.1.0'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='scientific_plots',
    packages=find_packages(),
    include_package_data=True,
    version=__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Scientific Plots - Matplotlib Journal Styles",
    author='Nils R Winter',
    author_email='nils.r.winter@gmail.com',
    url='https://github.com/NilsWinter/scientific_plots.git',
    download_url='https://github.com/NilsWinter/scientific_plots/archive/' + __version__ + '.tar.gz',
    keywords=['python', 'matplotlib', 'plots'],
    classifiers=["License :: OSI Approved :: MIT License",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence",
                 "Intended Audience :: Science/Research"],
    install_requires=['matplotlib',
                      'seaborn']
)