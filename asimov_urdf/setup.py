import os
from glob import glob 
from setuptools import find_packages, setup

package_name = 'asimov_urdf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', 'asimov_urdf', 'launch'), glob('launch/*.py')),
        (os.path.join('share', 'asimov_urdf', 'meshes'), glob('meshes/*')),
        (os.path.join('share', 'alpha_bot', 'config'),glob('config/*')),
        (os.path.join('share', package_name, 'asimov_urdf'), glob('asimov_urdf/*.urdf')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='naveen',
    maintainer_email='naveengnanasekar64@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
