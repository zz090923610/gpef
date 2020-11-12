from setuptools import setup



setup(
    name="gpef",
    version="0.0.1",
    description="General Purpose Experiment Framework",
    author='zhaozhang',
    author_email='zz156@georgetown.edu',
    packages=['gpef.tools', 'gpef.graphic', 'gpef.stat'],
    #install_requires=["matplotlib"],
    entry_points="""
    [console_scripts]
    cdf_plot = gpef.graphic.cdf_plot:main
    gpef = gpef.cmd.cmd:main
    basic_stat = gpef.stat.basic_stat:main
    """,
    install_requires=[
        "matplotlib",
        "pandas",
        "paramiko"
    ]
)
