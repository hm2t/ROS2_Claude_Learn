from setuptools import find_packages, setup

package_name = 'py_interface_demo'

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
    maintainer='hmt',
    maintainer_email='mingtaoh40@gmail.com',
    description='ROS2 自定义接口演示包 - 演示 msg/srv/action 三种通信方式',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher_node = py_interface_demo.publisher_node:main',
            'subscriber_node = py_interface_demo.subscriber_node:main',
            'service_server_node = py_interface_demo.service_server_node:main',
            'service_client_node = py_interface_demo.service_client_node:main',
            'action_server_node = py_interface_demo.action_server_node:main',
            'action_client_node = py_interface_demo.action_client_node:main',
        ],
    },
)
