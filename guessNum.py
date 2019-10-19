# -*- coding:utf_8 -*-
from log import logger
import random
if __name__ == '__main__':
    chance = 3
    result = int(random.random() * 10)
    logger.info(result)
    while True:
        num = int(input("猜猜我心里想的是什么数字？[0-9],你有%d次机会。" % chance))
        if num == result:
            logger.info("牛逼，真是个人才，你猜对了！！！")
            break
        chance -= 1
        if chance == 0:
            logger.info("你没有机会了，挑战失败。")
            break
        if num < result:
            logger.info("提示：太小了")
        if num > result:
            logger.info("提示：太大了")
    

        logger.info('猜错了，还有 %d次机会。' % chance)

    logger.info('游戏结束')