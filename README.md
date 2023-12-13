# Pork_Python

## 这是一个说明文档，这是pork项目的python版本

### Vison_Part 使用说明

    主要功能在process.py中, 使用时from process import * 
    
    1. updateScreen():
    获取屏幕截图并更新Game类, 主程序中定期调用或者在任何需要获取图像的时候调用;

    2. initPlayers():
    在叫地主抢地主阶段结束后调用初始化玩家数据;

    3. playCards(position, played_cards=None):
    position: 0, 1, 2, 代表自己, 下一个玩家, 上一个玩家
    played_cards: 一个长度为15的list, 表示打出的手牌. 自己打出的手牌请手动记录并传入, 其他玩家打出的手牌会自动获取(调用前请先updateScreen), played_cards位置不传参数

    4. getLastPlayedCards(position=None):
    position: 0, 1, 2, 代表自己, 下一个玩家, 上一个玩家
    不传入参数时返回一个长度为15的list, 表示上一次出牌的手牌, 传入参数时返回一个长度为15的list, 表示上一次该玩家出牌的手牌

    5. getSelfCardPostion(rank):
    rank: 0-14, 代表牌的大小, 0代表3, 1代表4, 以此类推
    返回一个包含了所有该大小牌的位置(x, y)的list, 如果牌有多张, 则返回多个位置, 没有则为空列表, 可以据此判断是否有该牌

    6. getRestCards():
    返回一个长度为15的list, 表示总牌库中剩余的牌, 0代表3, 1代表4, 以此类推

    7. getSelfButtonPosition(button):
    button: 按钮名称, 叫地主: claim, 不叫: no_claim, 出牌: play, 不出: pass
    返回一个(x, y)的tuple, 表示该按钮的位置

### AI_part 部分使用说明

    主要使用step()函数，来对当前的牌组进行更新，以达到预测的作用
    
### UI 部分使用说明

    该部分采用的多线程程序，加快运算速度，可以使用qt进一步优化
