import socket
import re
import random
import time

AIname = "Alice"
ServerAddress= "127.0.0.1"
ServerPort=10001

class TexCore:

    def __init__(self):
        self.totalChip = 200000  # 当前筹码数
        self.expectRate = 0.8  # 允许下注的筹码
        self.gameStatus = 0  # 游戏阶段 第n轮下注
        self.isBigblind = 0  # 1-大盲注 0小盲注
        self.nowRaise = 0  # 当前加注金额
        self.receiveFlag = 1  # 是否在接收状态
        self.respone = ''
        self.currentScore = 0

    def NameHandel(self):
        self.receiveFlag = 0
        self.respone = AIname
        return

    def PrefHandel(self,posi,cards):

        self.gameStatus=1
        self.isBigblind=posi
        self.handCards=cards

        self.GetCardValue()

        if self.isBigblind== 0:#小盲注直接从call开始
            self.receiveFlag=0
            self.respone = 'call'

        else :                  #玩家是大盲注
            self.receiveFlag = 1  # 等待对手
            self.nowRaise = 200
            self.respone = 'raise ' + str(self.nowRaise)

        return
        #这里是给牌进行估值

    def FlopHandel(self,cards):

        self.gameStatus = 2
        self.nowRaise = 0
        self.flopCards = cards

        self.GetCardValue()

        if self.isBigblind == 1:  #大盲注 先默认过牌
            self.receiveFlag = 0
            if self.currentScore == 0:
                self.respone = 'check'
            else:
                self.nowRaise = 400
                self.respone = 'raise ' + str(self.nowRaise)

        else:
            self.receiveFlag = 1  # 等待对手


    def TurnHandel(self,cards):

        self.gameStatus = 3
        self.nowRaise=0
        self.turnCards=cards

        self.GetCardValue()

        if self.isBigblind == 1:  #大盲注 过牌或者默认来两百
            self.receiveFlag = 0
            if self.currentScore>3 and self.nowRaise<8000:
                self.nowRaise = 200
                self.respone='raise ' + str(self.nowRaise)
            else:
                self.respone='check'

        else:
            self.receiveFlag = 1  # 等待对手

    def RiverHandel(self,cards):

        self.gameStatus = 4
        self.nowRaise = 0
        self.riverCards = cards

        self.GetCardValue()
        if self.isBigblind == 1:  # 大盲注 过牌或者默认来两百
            self.receiveFlag = 0
            if self.currentScore>2 and self.nowRaise < 8000:
                self.nowRaise = 200
                self.respone = 'raise ' + str(self.nowRaise)
            else:
                self.respone = 'check'

        else:
            self.receiveFlag = 1  # 等待对手

    def CallHandel(self):
        #收到盲注之后就会收到他，所以这里要干两件事
        #respone在之前prefhandl已经配置完了
        self.receiveFlag = 0
        return

    def RaiseHandel(self, count):
        #精髓
        self.receiveFlag = 0
        self.nowRaise=count
        if game.gameStatus==1: #盲注阶段就默认跟
            #self.receiveFlag = 0
            self.respone='call'

        else:
            if self.currentScore>4 :
            #if random.random() > 0.5:
                if self.nowRaise<6000:
                    self.nowRaise = self.nowRaise*2+random.randint(1,10)
                    self.respone='raise ' + str(self.nowRaise)  # 准备一个默认回复
                else:
                    self.respone = 'allin'
            elif self.currentScore>1:
                if self.nowRaise<5000:
                    self.nowRaise = self.nowRaise*2+random.randint(1,10)
                    self.respone='raise ' + str(self.nowRaise)  # 准备一个默认回复
                else:
                    self.respone = 'call'
            elif self.currentScore<2:
                if self.nowRaise<5000:
                    self.respone='call'
                else:
                    self.respone = 'fold'
            else:
                self.respone = 'call'

    def CheckHandel(self):
        self.receiveFlag = 1
        self.nowRaise = 0
        if self.gameStatus == 1:
            self.receiveFlag = 0
            self.respone = 'call'
        elif ((self.currentScore > 0) and self.nowRaise<5000):
            self.receiveFlag = 0
            self.nowRaise = 200
            self.respone = 'raise ' + str(self.nowRaise)  # 准备一个默认回复
        else:
            self.receiveFlag = 0
            self.respone = 'call'

    def AllinHandel(self):
        self.receiveFlag = 0
        if self.currentScore>3:
            self.respone = 'call'
        else:
            self.respone = 'fold'

    def GetRespone(self):
        self.receiveFlag = 1
        return self.respone

    def GetCardValue(self):
        #每阶段只调用一次
        self.currentScore = 0

        if self.gameStatus == 1:
            if self.handCards[0][1]==self.handCards[1][1]:
                self.currentScore += 1
            if self.handCards[0][1]>7 or self.handCards[0][1]>7:
                self.currentScore += 1

        if self.gameStatus == 2:
            for each in self.flopCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 2#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 4#潜在的三条 两对
            flopMax = max(self.flopCards[0][1],self.flopCards[1][1],self.flopCards[2][1])
            handMax = max(self.handCards[0][1],self.handCards[1][1])
            if handMax>flopMax:#手中最大大于公共最大
                self.currentScore += 1
            if self.flopCards[0][0] == self.flopCards[1][0] == self.flopCards[2][0]:
                if self.handCards[0][0] == self.flopCards[0][0]:
                    self.currentScore+=1
                if self.handCards[1][0] == self.flopCards[0][0]:
                    self.currentScore += 1
            if any([self.flopCards[0][0] == self.flopCards[1][0],
                    self.flopCards[0][0] == self.flopCards[2][0],
                    self.flopCards[1][0] == self.flopCards[2][0]]):
                self.currentScore += 1

        if self.gameStatus == 3:
            for each in self.flopCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 1#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 2#潜在的三条 两对

            for each in self.turnCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 1#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 2#潜在的三条 两对

            Max = max(self.turnCards[0][1],self.flopCards[0][1],self.flopCards[1][1],self.flopCards[2][1])

            handMax = max(self.handCards[0][1],self.handCards[1][1])
            if handMax>Max:#手中最大大于公共最大
                self.currentScore += 1
            if self.flopCards[0][0] == self.flopCards[1][0] == self.flopCards[2][0]:
                if self.handCards[0][0] == self.flopCards[0][0]:
                    self.currentScore+=1
                if self.handCards[1][0] == self.flopCards[0][0]:
                    self.currentScore += 1
            if any([self.flopCards[0][0] == self.flopCards[1][0],
                    self.flopCards[0][0] == self.flopCards[2][0],
                    self.flopCards[1][0] == self.flopCards[2][0]]):
                self.currentScore += 1

        if self.gameStatus == 4:
            for each in self.flopCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 1#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 2#潜在的三条 两对

            for each in self.turnCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 1#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 2#潜在的三条 两对

            for each in self.riverCards:
                if each[1] == self.handCards[0][1]:
                    self.currentScore += 1#潜在的两条 两对
                if each[1] == self.handCards[1][1]:
                    self.currentScore += 2#潜在的三条 两对

            Max = max(self.turnCards[0][1],self.flopCards[0][1],self.flopCards[1][1],self.flopCards[2][1])

            handMax = max(self.handCards[0][1],self.handCards[1][1])
            if handMax>Max:#手中最大大于公共最大
                self.currentScore += 1
            if self.flopCards[0][0] == self.flopCards[1][0] == self.flopCards[2][0]:
                if self.handCards[0][0] == self.flopCards[0][0]:
                    self.currentScore+=1
                if self.handCards[1][0] == self.flopCards[0][0]:
                    self.currentScore += 1
            if any([self.flopCards[0][0] == self.flopCards[1][0],
                    self.flopCards[0][0] == self.flopCards[2][0],
                    self.flopCards[1][0] == self.flopCards[2][0]]):
                self.currentScore += 1

        else:
            pass
        print(str(self.gameStatus)+'估值'+str(self.currentScore))
        return

def MsgHandel(msg):
    respone = ''
    #patternCard = re.compile(r'<.*?,.*?>')#匹配<,>
    patternSuit = re.compile(r'<.*?,')#匹配<,
    patternRank = re.compile(r',.*?>')#匹配,>
    patternRaise = re.compile(r'raise.*')
    #patternCheck = re.compile(r'check.*')
    #patternAllin = re.compile(r'allin.*')

    if(msg[0:4] == 'name'):
        game.NameHandel()

    elif(msg[0:4] == 'pref'):
        #cards = patternCard.findall(msg)
        cardsInArray = [
            [int(patternSuit.findall(msg)[0][1:-1]),int(patternRank.findall(msg)[0][1:-1])],
            [int(patternSuit.findall(msg)[1][1:-1]),int(patternRank.findall(msg)[1][1:-1])]]
        game.PrefHandel(0 if 'SMALLBLIND'in msg else 1 ,cardsInArray)
        #respone = game.GetRespone()

    elif(msg[0:4] == 'flop'):

        cardsInArray = [
            [int(patternSuit.findall(msg)[0][1:-1]), int(patternRank.findall(msg)[0][1:-1])],
            [int(patternSuit.findall(msg)[1][1:-1]), int(patternRank.findall(msg)[1][1:-1])],
            [int(patternSuit.findall(msg)[2][1:-1]), int(patternRank.findall(msg)[2][1:-1])]]
        game.FlopHandel(cardsInArray)


    elif(msg[0:4] == 'turn'):

        cardsInArray = [
            [int(patternSuit.findall(msg)[0][1:-1]), int(patternRank.findall(msg)[0][1:-1])]]
        game.TurnHandel(cardsInArray)


    elif(msg[0:4] == 'rive'):

        cardsInArray = [
            [int(patternSuit.findall(msg)[0][1:-1]), int(patternRank.findall(msg)[0][1:-1])]]
        game.RiverHandel(cardsInArray)

    elif(msg[0:4] == 'earn'):
        game.__init__()
        pass
    elif(msg[0:4] == 'oppo'):
        pass

    #需要回复的命令
    if('call'in msg):
        #理论上只有盲注阶段会收到这个命令
        game.CallHandel()
        #respone = game.GetRespone()

    if ('raise' in msg):
        msg = patternRaise.findall(msg)[0]
        count = int(msg[6:])
        game.RaiseHandel(count)

    if ('check' in msg):
        #msg = patternCheck.findall(msg)[0]
        game.CheckHandel()

    if ('allin' in msg):
        #msg = patternAllin.findall(msg)[0]
        game.AllinHandel()
        #respone = game.GetRespone()

    else:
        pass
    return

if __name__=='__main__':
    print("晚自习系统开始啦啊啊啊啊啊啊啊啊啊啊")
    connectTex = socket.socket()
    connectTex.connect((ServerAddress, ServerPort))
    game = TexCore()
    print("链接创建成功，游戏实例化")

    while 1:
        while game.receiveFlag :
            msg = str(connectTex.recv(1024),encoding="utf-8")
            if msg != '':
                print("RX:"+msg)
                respone = MsgHandel(msg)
            if game.receiveFlag == 0 :
                respone = game.GetRespone()
                print("TX:" + respone)
                time.sleep(0.3)
                connectTex.send(respone.encode('utf-8'))


#connctTex.close()不太确定啥时候加
