from setuptools import setup

setup(
    name="snapshotalyzer",
    version="0.1",
    author="Vivek T",
    author_email="vivekthite@gmail.com",
    maintainer="Vivek T",
    maintainer_email="vivekthite@gmail.com",
    url="https://github.com/vivekthite/snapshotanalyzer",
    license="GPLv3+",
    description="This tool help us to take snaps of EC2 instances",
    packages=['scripts'],
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
            [console_scripts]
            ec2=scripts.ec2:cli
        '''
)