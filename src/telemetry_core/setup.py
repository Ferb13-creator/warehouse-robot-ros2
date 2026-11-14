from setuptools import find_packages, setup

package_name = 'telemetry_core'

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
        'service_server2=telemetry_core.service_server2:main',
        'service_client2=telemetry_core.service_client2:main',
        'action_server=telemetry_core.action_server:main',
        'action_client=telemetry_core.action_client:main',
        'battery_charger_server=telemetry_core.battery_charger_server:main',
        'battery_charger_client=telemetry_core.battery_charger_client:main',
        ]
    }    
)
