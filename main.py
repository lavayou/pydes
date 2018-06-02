from .permut_table import PC_1, SHIFT, PC_2, IP, E, S_BOX, FP, P
from .logger import logger


class DES(object):
    ENCRYPT = 1
    DECRYPT = 0

    def __init__(self, text=None, password=None, debug=False):
        self._keys = []
        self._password = password
        self._text = text
        self.__result = None
        self._method = None
        if debug is False:
            logger.setLevel(30)

    @property
    def text(self):
        return self._text

    @property
    def password(self):
        return self._password

    def start(self):
        self.generate_keys()
        logger.info('generated keys done, start 16 times rounds.')
        block = self.string_to_binary_string(self._text)
        logger.info('raw block: ' + str(block))
        block = self.permut(block, IP)
        logger.info('block after initial permutation: ' + str(block))
        l, r = self.split_to_parts(block, 32)
        temp = None

        for i in range(16):
            logger.info('start round ' + str(i) + ' permutation.')
            r_e = self.expand(r, E)
            logger.info('right part after expand permutation: ' + str(r_e))
            if self._method == self.ENCRYPT:
                temp = self.xor(self._keys[i], r_e)
                logger.info('after xor with key: ' + str(temp))
            else:
                temp = self.xor(self._keys[15 - i], r_e)
                logger.info('after xor with key: ' + str(temp))
            temp = self.s_box_replace(temp)
            logger.info('after SBOX replacement: ' + str(temp))
            temp = self.permut(temp, P)
            logger.info('after Permutation: ' + str(temp))
            temp = self.xor(temp, l)
            logger.info('after xor with left part' + str(temp))
            l = r
            r = temp
            logger.info('exchange left part and right part.')
            logger.info('round ' + str(i) + ' done, start next round.\n')
        logger.info('all round finished. exchange left part and right part.')
        l, r = r, l
        logger.info('exchang done, left part: ' + str(l))
        logger.info('exchang done, right part: ' + str(r))
        logger.info('start final permutation.')
        result = self.final_permut(l + r, FP)
        logger.info('result: ' + str(result))
        self.__result = result

    def generate_keys(self):
        key = self.string_to_binary_string(self.password)
        logger.info(
            'length of password before permuted choice 1: ' + str(len(key)))
        logger.info('password before permuted choice 1: ' + str(key))
        key = self.permut(key, PC_1)
        logger.info(
            'length of password after permuted choice 1: ' + str(len(key)))
        logger.info('password after permuted choice 1: ' + str(key))
        l, r = self.split_to_parts(key, 28)
        for i in range(16):
            l, r = self.shift(l, r, SHIFT[i])
            temp = l + r
            temp_key = self.permut(temp, PC_2)
            logger.info(
                'generated key ' + str(i) + ' with permutation choice 2 ' + str(
                    temp_key))
            self._keys.append(temp_key)

    def encrypt(self):
        self._method = self.ENCRYPT
        if self.__check_arguments():
            self.start()
            return self.binary_string_to_string(self.__result)
        else:
            logger.info('arguments invalid. check it.')

    def decrypt(self):
        self._method = self.DECRYPT
        if self.__check_arguments():
            self.start()
            return self.binary_string_to_string(self.__result)
        else:
            logger.info('arguments invalid. check it.')

    def __check_arguments(self):
        if self.__check_text() and self.__check_password():
            return True
        else:
            return False

    def __check_password(self):
        if len(self._password) == 8 and isinstance(self._password, str):
            return True
        else:
            raise ValueError('password to long or too short.')

    def __check_text(self):
        if len(self._text) == 8 and isinstance(self._text, str):
            return True
        else:
            raise ValueError('text to long or too short.')

    def s_box_replace(self, r_e):
        '''S盒子中，以 b1 和 b6 确定行，以 b2 和 b5 确定列。 在这里由于没有仔细看书，
        造成了最后的问题出现。'''
        sub_blocks = self.split_to_parts(r_e, 6)
        result = []
        for i in range(len(sub_blocks)):
            block = sub_blocks[i]
            row = int(str(block[0]) + str(block[5]), 2)
            column = int(
                str(block[1]) + str(block[2]) + str(block[3]) + str(block[4]),
                2)
            val = S_BOX[i][row][column]
            val = self.character_to_bin_string(val, 4)
            val = [int(x) for x in val]
            result.extend(val)
        return result

    @staticmethod
    def permut(block, table):
        '''置换函数'''
        return [block[n - 1] for n in table]

    @staticmethod
    def expand(block, table):
        ''' 同permut函数，但是更具可读性 '''
        return [block[n - 1] for n in table]

    @staticmethod
    def final_permut(block, table):
        ''' 同permut函数，但是更具可读性 '''
        return [block[n - 1] for n in table]

    @staticmethod
    def shift(l, r, n):
        return l[n:] + l[:n], r[n:] + r[:n]

    @staticmethod
    def split_to_parts(key, size_of_part):
        return [key[k:k + size_of_part] for k in
                range(0, len(key), size_of_part)]

    def string_to_binary_string(self, text):
        """将字符串转化为形如 [0,1,0,1,0,1,0...] 形式的数组"""
        binstring = []
        for char in text:
            binval = self.character_to_bin_string(char, 8)
            binstring.extend([int(x) for x in list(binval)])
        return binstring

    @staticmethod
    def character_to_bin_string(val, length):
        """转换 单个字符 or 数字 到二进制字符串"""
        binstring = bin(ord(val))[2:] if isinstance(val, str) else bin(val)[2:]
        while len(binstring) < length:
            binstring = '0' + binstring
        return binstring

    def binary_string_to_string(self, bin_string):
        bytes = self.split_to_parts(bin_string, 8)
        result = ''
        for byte in bytes:
            byte = ''.join([str(x) for x in byte])
            char = chr(int(byte, 2))
            result = result + char
        return result

    @staticmethod
    def xor(a, b):
        return [x ^ y for x, y in zip(a, b)]


if __name__ == '__main__':
    encrypted_data = DES(text='Molly Wu', password='programs').encrypt()
    print(encrypted_data)
    decrypted_data = DES(text=encrypted_data, password='programs').decrypt()
    print(decrypted_data)
