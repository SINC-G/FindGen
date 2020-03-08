#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
测试生成区块。

@File    :   generate_block_test.py
@Time    :   2020/02/19 15:51:30
@Author  :   ZHOU 
"""

import json
from blockchain import block
from blockchain.blockchain import BlockChain
from gfw.generater import adress
from gfw.generater import goodsid
from gfw.records import record


def main():
    """
    区块生成流程。

    生产者:生成参与者地址->商品地址生成->记录生成->生成区块(共识算法参与)->上链(区块链,redis,通信等问题)
    """
    producer=adress.Partner() # 生产者实例化
    producer.new_keypair() # 生产者公私钥对生成
    
    pgid_worker=goodsid.IdWorker(69012345678912,0) # TODO(ZHOU) 输入没有校验（EAN13码是有校验功能的，此程序还未实现）
    goods_1=pgid_worker.get_id() # 生成一个商品ID

    rec=record.Record(goods_1,producer.private_key,producer.pub_key) # 实例化记录处理程序
    r_1=rec.new_record(0x0) # 生成一条记录
    recs=[]
    recs.append(r_1)

    blo=block.Block() #实例化区块生成程序
    blo_1=blo.new_block(recs,'0') # 生成区块

    bolockchain=BlockChain() # 实例化区块链
    bolockchain.add_block(blo_1) # 添加区块到区块链中


if __name__ == "__main__":
    main()


# TODO(ZHOU) 包编程问题
# TODO(ZHOU) 可以增加些校验