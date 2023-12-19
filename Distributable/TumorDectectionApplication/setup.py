from gettext import install
import setuptools import find_packages, setup

setuptools.setup(
    include_package_data=True,
    name='TumorDetectionApplication',
    version='1.0.0',
    description='This is the first iteration of an AI Tumor Detection Application',
    url='https://github.com/MintyMika/CS458_Brain_Tumor_Detection/tree/main/Distributable',
    author='CS458BrainCancer',
    author_email='cs458braincancer@gmail.com',
    packages=setuptools.find_packages(),
    #install_requires=[],
    #long_description='Testing of Distributable',
    classifiers=[
        "Programming Language :: Python"
    ]
)