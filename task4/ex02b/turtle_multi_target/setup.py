import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtle_multi_target'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='chernodolja@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'target_switcher = turtle_multi_target.target_switcher:main',
            'turtle_controller = turtle_multi_target.turtle_controller:main',
            'turtle_tf2_broadcaster = turtle_multi_target.turtle_tf2_broadcaster:main',
        ],
    },
)
