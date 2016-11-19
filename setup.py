from setuptools import setup, find_packages 
from os import path, walk


here = path.abspath(path.dirname(__file__))
datadir = 'kriging'
package_data = [ (d, [path.join(d, f) for f in files]) for d,folders,files in walk(datadir)]
data_files=[]
for i in package_data:
    for j in i[1]:
        data_files.append(j)
data_files = [path.relpath(file, datadir) for file in data_files]

setup(
    name='kriging',
    version='1.0',
    zip_safe = False,
    packages=find_packages(),
    package_data={'kriging': ['kriging/*']},
    license='',
    author='Suraj Sanka, Mrinal Patil, Vinod Kumar',
    description='A Kriging Toolbox for Python',
    install_requires=['scipy', 'numpy', 'matplotlib', 'inspyred'],
)
