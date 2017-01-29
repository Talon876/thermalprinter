from setuptools import setup

required_packages = open('requirements.txt', 'r').readlines()

setup(
    name='tprinter',
    version='0.0.1',
    description='Prints images and text on a thermal printer',
    packages=['tprinter', 'tprinterbot'],
    install_requires=required_packages,
    include_package_data=True,
    entry_points= {
        'console_scripts': [
            'irclurker=tprinterbot:irclurker.main'
        ]
    }
)

