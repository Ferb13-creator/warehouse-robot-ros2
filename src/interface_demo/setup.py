from setuptools import find_packages, setup

package_name = 'interface_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ferb',
    maintainer_email='ferb@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
    'status_publisher = interface_demo.status_publisher:main',
    'status_subscriber = interface_demo.status_subscriber:main',
    'speed_server = interface_demo.speed_server:main',
    'speed_client = interface_demo.speed_client:main',
    'move_action_server = interface_demo.move_action_server:main',
    'move_action_client = interface_demo.move_action_client:main',
],
    },
)
