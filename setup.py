from distutils.core import setup

setup(name='modbus-python',
      version='1.0',
      description='driver for modbus to interface with RS 485 - USB  module',
      author='Rahulkannan S',
      author_email='srahulkannan63@gmail.com',
      url='https://github.com/rahulknns/modbus-python.git',
      install_requires=["serial"],
      packages=['modbus_frames', 'modbus_rtu'],
     )


