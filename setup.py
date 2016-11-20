from distutils.core import setup

requires = ["numpy",
            "scipy",
            "inspyred",
            "Tkinter"]

setup(name='kriging',
      version='0.1',
      description='Curve fitting tool',
      author='Suraj Sanka, Mrinal Patil, Vinod Kumar',
      author_email='sankasuraj@gmail.com',
      license='License',
      install_requires=requires,
      packages=['kriging'],
      )
