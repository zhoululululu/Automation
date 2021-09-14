# -*- coding: utf-8 -*-
"""
Created on 2021/7/19 9:40
@File  : encrypt_tool.py
@author: zhoul
@Desc  :
"""
import hashlib
import base64
from Cryptodome.Cipher import AES


class EncryptTool:

    @classmethod
    def md5_encode(cls, text):
        """
        md5加密，32位
        :param text:
        :return:
        """
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()

    @classmethod
    def base64_encode(cls, text):
        return base64.b64encode(bytes(text))

    @classmethod
    def base64_decode(cls, base64_text):
        return base64.b64decode(base64_text)

    @classmethod
    def aes_encrypt_with_cbc(cls, text: str, key: str, iv: str):
        """
        AES的CBC模式加密,返回base64
        @param text: 待加密字符串
        @param key: 加密密码
        @param iv: 初始化向量
        @return:
        """
        mode = AES.MODE_CBC
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        # 文本用空格补足为16位
        remainder = len(text.encode('utf-8')) % 16
        if remainder:
            text = text + '\0' * (16 - remainder)
        cipher = AES.new(key, mode, iv)
        cipher_text = cipher.encrypt(text.encode('utf-8'))
        return cls.base64Encode(cipher_text).decode('utf-8')

    @classmethod
    def aes_decrypt_with_cbc(cls, encrypt_text: str, key: str, iv: str):
        """
        AES的CBC模式解密
        @param encrypt_text: 待解密字符串,base64
        @param key: 加密密码
        @param iv: 初始化向量
        @return:
        """
        mode = AES.MODE_CBC
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        cipher = AES.new(key, mode, iv)
        text = cipher.decrypt(cls.base64Decode(encrypt_text))
        return text.decode('utf-8')

    @classmethod
    def aes_encrypt_with_ecb(cls, text: str, key: str):
        """
        AES的ECB模式加密,返回base64
        @param text: 待加密字符串
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        key = key.encode('utf-8')
        # 文本用空格补足为16位
        remainder = len(text.encode('utf-8')) % 16
        if remainder:
            text = text + '\0' * (16 - remainder)
        cipher = AES.new(key, mode)
        cipher_text = cipher.encrypt(text.encode('utf-8'))
        return cls.base64Encode(cipher_text).decode('utf-8')

    @classmethod
    def aes_decrypt_with_ecb(cls, encrypt_text: str, key: str):
        """
        AES的CBC模式解密
        @param encrypt_text: 待解密字符串,base64
        @param key: 加密密码
        @return:
        """
        mode = AES.MODE_ECB
        key = key.encode('utf-8')
        cipher = AES.new(key, mode)
        text = cipher.decrypt(cls.base64Decode(encrypt_text))
        return text.decode('utf-8')


if __name__ == '__main__':
    print(EncryptTool.md5_encode('/api/v2/Consignment|{"recipientName":"","country":"","state":"","city":"","addressLine1":"","postcode":"","weight":"","facility":""}|0639285a-0ec4-11ec-82a8-0242ac130003|c276a773-7ec5-4e6c-8d80-95f21ec858e0'))
