from .main import DES

# Author:      lavayou
# Date:        2nd June, 2018
# Version:     0.1
# Description: 'A very very simple implementation of DES encryption and decryption '
# References:   https://github.com/RobinDavid/pydes
#               https://en.wikipedia.org/wiki/DES_supplementary_material
#               https://en.wikipedia.org/wiki/DES
#               《计算机网络安全基础》
#
# Class initialization:
#       text : The text you want to encrypt or decrypt.
#           default:    None
#           available:  8 Bytes string
#
#       password: The password for decrypt or encrypt text.
#           default: None
#           available:  8 Bytes string
#
#       debug: print running information to ./log/des.log file.
#           default: False
#
# How to Use:
#   from pydes import DES
#   decrypted_data = DES(text='È¨©k', password='programs').decrypt()
#   print(decrypted_data)
#
#
# Notice: This implementation now only support 8 letters string.