# -*- coding: utf-8 -*-
from world_model import World
from world_model import Vector2D
from world_model import Line2D
from world_model import Rect2D
from world_model import Circle2D

import csv

'''
スルーパスの解析をするスクリプト
スルーパスを出す選手の座標、スルーパスを受け取る選手（受け取った瞬間の）座標、スルーパス時に近い相手選手２人の座標
をcsvファイルに格納します。
'''




'''
フィールド相手側を分割し、引数の座標がどこに含まれているかを返す関数
1   21  .   .   181
2   22  .   .   .
3   23  .   .   .
.   .   .   .   .
.   .   .   .   .
.   .   .   .   .
20  40  .   .   200
'''
def getRectNumber( axis ):

    rects = []
    for j in range(10):
        for i in range(20):
            top_left = Vector2D( 0.0 + j * 5.25, -34.0 + i * 3.4 )
            bottom_right = Vector2D( top_left.x + 5.25, top_left.y + 3.4 )

            rects.append(Rect2D( top_left, bottom_right))

    for i in range( len(rects) ):
        if rects[i].contains(axis):
            return i + 1
    
    return -1


if __name__ == '__main__':
    # ワールドモデルのインスタンス生成
    wm = World()

    # キッカーの情報を格納
    kicker = None
    # キッカーがボールを蹴ったサイクル
    kick_cycle = 6000
    
    # スルーパスが成立していたらTrue
    was_through_pass = False

    # ファイルに書き出す
    f = open('through_pass.csv', 'a')
    writer = csv.writer(f, lineterminator='\n')

    # ゲームループ(1サイクルから6000サイクルまで)
    while wm.time().kick_off() <= wm.time().cycle() \
            and wm.time().cycle() <= wm.time().time_over():

        # 味方ボールかつ試合中
        if wm.lastKickerSide() == "left" \
        and wm.gameMode().type() == "play_on":
            # 味方にスルーパスを出した選手がまだいないとき
            if kicker is None \
            and wm.existKickableTeammate() \
            and wm.getTeammateNearestToBall( False ).Action() == "kick":
                kicker = wm.getTeammateNearestToBall( False )
                kick_cycle = wm.time().cycle()

            # 味方にボールを蹴った選手がいるとき
            elif kicker is not None \
            and wm.getTeammateNearestToBall( False ).Action() == "kick" \
            and kicker.unum() != wm.getTeammateNearestToBall( False ).unum(): # パスを出した選手とパスを受け取った選手が違う選手のとき
                if wm.getTeammateNearestToBall( False ).pos().x > wm.theirDefenseLineX() - 0.5: # ボールを受け取った場所が相手のディフェンスライン付近のときは99%スルーパス
                    
                    # スルーパス成立
                    was_through_pass = True
                    
                    # スルーパスを受け取った選手の情報
                    receiver = wm.getTeammateNearestToBall( False )
                    
                    print "cycle : ", kick_cycle
                    print "passer : ", kicker.unum()
                    print "receiver : ", wm.getTeammateNearestToBall( False ).unum()
                    print ""
                    
                    csvlist = []
                    # csvlist.append( kicker.pos().x ) # 1. パス蹴った味方選手の位置X [パス出したサイクル]
                    # csvlist.append( kicker.pos().y ) # 1. パス蹴った味方選手の位置Y [パス出したサイクル]
                    csvlist.append( getRectNumber(kicker.pos()) )
                    
                    # csvlist.append( wm.ourPlayer(receiver.unum(), kick_cycle).pos().x ) # 2. パス受け取った味方選手の位置X [パス出したサイクル]
                    # csvlist.append( wm.ourPlayer(receiver.unum(), kick_cycle).pos().y ) # 2. パス受け取った味方選手の位置Y [パス出したサイクル]
                    csvlist.append( getRectNumber(wm.ourPlayer(receiver.unum(), kick_cycle).pos()) )
                    
                    # csvlist.append( receiver.pos().x ) # 3. パス受け取った味方選手の位置X [パスを受け取ったサイクル]
                    # csvlist.append( receiver.pos().y ) # 3. パス受け取った味方選手の位置Y [パスを受け取ったサイクル]
                    csvlist.append( getRectNumber(receiver.pos()) )
                    
                    theirPlayer_pos = [ wm.theirPlayer(i, kick_cycle).pos() for i in range(1, 12) ] # 2番~11番の相手選手の座標
                    theirPlayer_pos.append( Vector2D(wm.ourPlayer(receiver.unum(), kick_cycle).pos().x, -34.0) )
                    theirPlayer_pos.append( Vector2D(wm.ourPlayer(receiver.unum(), kick_cycle).pos().x, 34.0) )

                    theirPlayer_pos = sorted(theirPlayer_pos, key=lambda x: x.dist(wm.ourPlayer(receiver.unum(), kick_cycle).pos())) # 上の2. に近い順にソート

                    nearest_opp = theirPlayer_pos[0] # 2. に一番近い選手を格納する
                    second_opp = theirPlayer_pos[1] # 2. に一番近い選手を格納する

                    ave_pos = Vector2D((nearest_opp.x + second_opp.x) / 2, (nearest_opp.y + second_opp.y) / 2)
                    # csvlist.append( ave_pos.x ) # 4. 2.に近い選手２人の平均座標X
                    # csvlist.append( ave_pos.y ) # 4. 2.に近い選手２人の平均座標Y
                    csvlist.append( getRectNumber(ave_pos) )

                    writer.writerow(csvlist)
                    csvlist = []
                    theirPlayer_pos = []

                kicker = None

            # 味方がドリブルをしているときはキッカーの情報を更新
            elif kicker is not None \
            and wm.getTeammateNearestToBall( False ).Action() == "kick" \
            and kicker.unum() == wm.getTeammateNearestToBall( False ).unum(): # パスを出した選手とパスを受け取った選手が同じ選手(ドリブル中)のとき
                kicker = wm.getTeammateNearestToBall( False )
                kick_cycle = wm.time().cycle()
        
        # 相手ボール時やファウルなどで試合が中断しているときはキッカーの情報を破棄
        else:
            kicker = None

        # プレーモードを更新
        wm.gameMode().UpdatePlayMode()

        # サイクルを1進める
        wm.time().addTime()

    f.close()
