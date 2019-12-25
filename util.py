from pyDes import des,CBC,PAD_PKCS5
import binascii

class Util():
    def des_encrypt(s):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """
        KEY = 'abcdefgh'
        secret_key = KEY
        iv =secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        re=binascii.b2a_hex(en)
        re2=str(re,encoding='utf-8')
        return re2


    def des_descrypt(s):
        """
        DES 解密
        :param s: 加密后的字符串，16进制
        :return:  解密后的字符串
        """
        KEY = 'abcdefgh'
        secret_key = KEY
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
        de2=str(de,encoding='utf-8')
        return de2