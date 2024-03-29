#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
生成参与者的地址。
先创建公私钥对，再生成地址，之后加密。

@File    :   adress.py
@Time    :   2020/02/07 19:33:02
@Author  :   ZHOU 
"""

import hashlib
import json
from fastecdsa import keys, curve
from crypto.base58 import base58encode, base58decode

version = "0x"
addressChecksumLen = 4
WalletFile = "wallet.txt"

class Participant(object):
    """
    生成参与者地址
    """

    def __init__(self):
        self.pub_key = None
        self.priv_key = None
        self.address = None

    def get_adress(self):
        """
        返回地址。
        :return:地址
        """
        priv_key, pub_key = self.priv_key,self.pub_key
        pubkey_hash = self.hash_pk(pub_key)
        version_payload = "".join([str(version), str(pubkey_hash)])
        checksum = self.checksum(version_payload)

        full_payload = "".join([str(version_payload), str(checksum)])

        adress=full_payload
        address = base58encode(full_payload)
        self.address=address
        return adress

    def new_keypair(self):
        """
        生成公私钥的键值对
        :return :返回公私钥。
        """
        priv_key = keys.gen_private_key(curve.P256) # 私钥只能int型，来生成公钥

        pub_key = keys.get_public_key(priv_key, curve.P256) # 公钥可以byte，bytearray, str，来生成地址
        # print(type(pub_key))

        pub_key = "".join([str(pub_key.x), str(pub_key.y)])

        self.priv_key = priv_key
        self.pub_key = pub_key
        return priv_key, pub_key

    def hash_pk(self, pub_key):
        """
        公钥加密
        :param pub_key:
        :return:
        """
        if not isinstance(pub_key, (bytes, bytearray, str)):
            raise TypeError("pub 类型错误，需要str 或者bytes类型！")

        if isinstance(pub_key, str):
            pub_key = pub_key.encode("utf-8")

        # sha256 加密
        pub_sha256 = hashlib.sha256(pub_key).hexdigest()

        # ripemd160
        obj = hashlib.new("ripemd160", pub_sha256.encode('utf-8'))
        ripemd160_value = obj.hexdigest()

        return ripemd160_value

    # 校验和
    def checksum(self, payload):
        if not isinstance(payload, (bytes, bytearray, str)):
            raise TypeError("payload 类型错误，需要str 或者bytes类型！")

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        first_sha = hashlib.sha256(payload).hexdigest()
        second_sha = hashlib.sha256(first_sha.encode('utf-8')).hexdigest()

        return second_sha[:addressChecksumLen]

    def validate_addr(self, address):
        """
        :return:
        """
        pub_key_hash = base58decode(address)
        pub_key_hash=address

        actural_check_sum = pub_key_hash[len(pub_key_hash) - addressChecksumLen:]
        version = pub_key_hash[0]
        pub_key_hash = pub_key_hash[1:len(pub_key_hash) - addressChecksumLen]

        payload = "".join([str(version), str(pub_key_hash)])

        target_check_sum = self.checksum(payload)

        return actural_check_sum == target_check_sum

    # 将私钥保存到文件中
    def save_to_file(self):
        priv_key=self.priv_key
        if not isinstance(priv_key,str):
            priv_key=str(priv_key)
        with open(WalletFile, 'w') as f:
            pri_dict = {
                'PrivateKey':base58encode(priv_key)
            }
            f.write(json.dumps(pri_dict)+'\n')
    
    # 从文件中读取私钥,并构建公钥与地址
    def load_to_file(self):
        wallets = dict()
        with open(WalletFile, 'r') as f:
            for line in f.readlines():
                line_dict = json.loads(line)
                print(base58encode(line_dict['PrivateKey']))
                #priv_key = int()
        pub_key = keys.get_public_key(priv_key, curve.P256)
        pub_key = "".join([str(pub_key.x), str(pub_key.y)])
        self.priv_key = priv_key
        self.pub_key = pub_key
        return self.get_adress()


# 测试
if __name__=='__main__':
    producer=Participant() #生产者

    p1=producer.get_address()
    print(p1)
    print(producer.priv_key)
    producer.save_to_file()