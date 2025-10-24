from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'lab4_tf2'

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
            'static_turtle_tf2_broadcaster = lab4_tf2.static_turtle_tf2_broadcaster:main',
            'turtle_tf2_broadcaster = lab4_tf2.turtle_tf2_broadcaster:main',
            'turtle_tf2_listener = lab4_tf2.turtle_tf2_listener:main',
            'fixed_frame_tf2_broadcaster = lab4_tf2.fixed_frame_tf2_broadcaster:main',
            'dynamic_frame_tf2_broadcaster = lab4_tf2.dynamic_frame_tf2_broadcaster:main',
        ],
    },
)
