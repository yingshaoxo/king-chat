from setuptools import setup, find_packages
from os.path import dirname, join, abspath

file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

setup(name='king_chat',
        version='0.0.3',
        description='This is a powerful chat center for all kinds of messages.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            ],
        url='https://github.com/yingshaoxo/king-chat',
        install_requires=['twisted'],
        author='yingshaoxo',
        author_email='yingshaoxo@gmail.com',
        license='GPLv3',
        packages=find_packages(),
        include_package_data=False,
        )
