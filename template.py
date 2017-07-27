# -*- coding: utf-8 -*-
from world_model import World
from world_model import Vector2D
from world_model import Line2D
from world_model import Rect2D
from world_model import Circle2D


if __name__ == '__main__':
    # create the instance of world_model
    wm = World()

    # kick_off cycle
    print "wm.time().kick_off() : ", wm.time().kick_off()
    # time_over or stop the game cycle
    print "wm.time().time_over() : ", wm.time().time_over()
    print "wm.fullstateTime() : ", wm.fullstateTime()

    # our team name
    print "TeamName: ", wm.teamName()

    # our score
    print "TeamScore: ", wm.gameMode().scoreLeft()

    # opponent team name
    print "OppName: ", wm.opponentTeamName()

    # opponent score
    print "OppScore: ", wm.gameMode().scoreRight()

    # Vector2D Class(float x, float y)
    point1 = Vector2D(0.0, 0.0)
    point2 = Vector2D(5.0, 5.0)

    point3 = Vector2D(0.0, 5.0)
    point4 = Vector2D(5.0, 10.0)

    # Line2D Class(Vector2D point1, Vector2D point2)
    line1 = Line2D(point1, point2)
    line2 = Line2D(point3, point4)

    # Circle2D Class(Vector2D center_pos, float radius)
    circle = Circle2D(point1, 9.0)

    # Rect2D Class(Vector2D top_left, Vector2D bottom_right)
    rect2d = Rect2D(point1, point2)

    # Center Coordinate of Circle2D
    print "circle.center()", (circle.center().x, circle.center().y)

    # if the circle contains Coordinate of the point, return True
    # else return False
    print "circle.contains(point)", circle.contains(point2)

    # calc perpendicular line (SUI-SEN)
    # Line Fomula: aX + bY + c = 0
    print "line.dist(Vector2D point)", line1.dist(point3)

    # the intersection point with 'line'
    # return intersection point. if it does not exist,
    # the invaidated value vector is returned.
    print "line1.intersection(line2)",\
        (line1.intersection(line2).x, line1.intersection(line2).y)

    # check if the slope of this line is same to the slope of 'line'
    # return true if almost same
    # else return False
    print "line1.isParallel(line2)", line1.isParallel(line2)

    # return coefficient 'A' of line formula
    print "line1.getA()", line1.getA()

    # return coefficient 'B'  of line formula
    print "line1.getB()", line1.getB()

    # return coefficient 'C'  of line formula
    print "line1.getC()", line1.getC()

    # if the rect2d contains point return True
    # else return False
    print "rect2d.contains(point)", rect2d.contains(point1)

    # center_point of Rect2D
    print "rect2d.center()", (rect2d.center().x, rect2d.center().y)

    # sys.exit()

    # Game loop(1 Cycle ~ 6000 Cycle) If the game was over halfway through, that cycle
    while wm.time().kick_off() <= wm.time().cycle() \
            and wm.time().cycle() <= wm.time().time_over():
        print ""
        print "---------------------------------" \
            "------------------------------------"

        # now Cycle
        print "wm.time().cycle()", wm.time().cycle()

        # the Coordinate of the ball
        print "wm.ball().pos().x(y)", (wm.ball().pos().x, wm.ball().pos().y)

        # get the distance from input point to the nearest opponent
        # param with_goalie include goalie if true
        # param point : Vector2D
        print "wm.getDistOpponentNearestTo(with_goalie, point1)", \
            wm.getDistOpponentNearestTo(True, point1)

        # get the distance to opponent nearest to ball
        # param with_goalie
        print "wm.getDistOpponentNearestToBall(with_goalie)",\
            wm.getDistOpponentNearestToBall(True)

        # get opponent pointer nearest to point(PlayerObject Class)
        # ex. (uniform number, is kickable ?, dist from ball, action)
        print "wm.getOpponentNearestTo(with_goalie, point)",\
            "unum = ", wm.getOpponentNearestTo(True, point1).unum(), \
            "isKickable = ", wm.getOpponentNearestTo(True, point1).isKickable(),\
            "distFromBall = ", wm.getOpponentNearestTo(True, point1).distFromBall(), \
            "Action = ", wm.getOpponentNearestTo(True, point1).Action()

        # get opponent nearest to ball
        # Usage is same as above wm.getOpponentNearestTo ()
        print "wm.getOpponentNearestToBall(with_goalie)",\
            "unum = ", wm.getOpponentNearestToBall(True).unum(), \
            "isKickable = ", wm.getOpponentNearestToBall(True).isKickable(), \
            "distFromBall = ", wm.getOpponentNearestToBall(True).distFromBall(), \
            "Action = ", wm.getOpponentNearestToBall(True).Action()

        # get the distance to teammate nearest to ball
        # param with_goalie include goalie if true
        # param point : Vector2D
        print "wm.getDistTeammateNearestTo(with_goalie, point1)", \
            wm.getDistTeammateNearestTo(True, point1)

        # get the distance to teammate nearest to ball
        # param with_goalie
        print "wm.getDistTeammateNearestToBall(with_goalie)", \
            wm.getDistTeammateNearestToBall(True)

        # get teammate pointer nearest to point(PlayerObject Class)
        # ex(uniform number, is kickable ?, dist from ball, action)
        print "wm.getTeammateNearestTo(with_goalie, point)",\
            "unum = ", wm.getTeammateNearestTo(True, point1).unum(),\
            "isKickable = ", wm.getTeammateNearestTo(True, point1).isKickable(),\
            "distFromBall = ", wm.getTeammateNearestTo(True, point1).distFromBall(),\
            "Action = ", wm.getTeammateNearestTo(True, point1).Action()

        # get teammate nearest to ball(PlayerObject Class)
        # Usage is same as wm.getTeammateNearestTo () above
        print "wm.getTeammateNearestToBall(bool with_goalie)",\
            "unum = ", wm.getTeammateNearestToBall(True).unum(),\
            "isKickable = ", wm.getTeammateNearestToBall(True).isKickable(),\
            "distFromBall = ", wm.getTeammateNearestToBall(True).distFromBall(),\
            "Action = ", wm.getTeammateNearestToBall(True).Action()

        # get an opponent specified by uniform number
        # ex.　opponent 11 player ( at this cycle )
        print "wm.theirPlayer(unum)",\
            "unum = ", wm.theirPlayer(11).unum(), \
            "isKickable = ", wm.theirPlayer(11).isKickable(), \
            "distFromBall = ", wm.theirPlayer(11).distFromBall(), \
            "Action = ", wm.theirPlayer(11).Action()

        # ex. opponent 6 player( at 116 cycle )
        print "wm.theirPlayer(unum)",\
            "unum = ", wm.theirPlayer(6, 116).unum(), \
            "isKickable = ", wm.theirPlayer(6, 116).isKickable(), \
            "distFromBall = ", wm.theirPlayer(6, 116).distFromBall(), \
            "Action = ", wm.theirPlayer(6, 116).Action()

        # get an teammate specified by uniform number
        # ex.　teammate 6 player ( at this cycle )
        print "wm.ourPlayer(unum)",\
            "unum = ", wm.ourPlayer(6).unum(), \
            "isKickable = ", wm.ourPlayer(6).isKickable(), \
            "distFromBall = ", wm.ourPlayer(6).distFromBall(), \
            "Action = ", wm.ourPlayer(6).Action()

        # ex.　teammate 9 player( at 426 cycle )
        print "wm.ourPlayer(unum)",\
            "unum = ", wm.ourPlayer(9, 426).unum(), \
            "isKickable = ", wm.ourPlayer(9, 426).isKickable(), \
            "distFromBall = ", wm.ourPlayer(9, 426).distFromBall(), \
            "Action = ", wm.ourPlayer(9, 426).Action()

        # get the opponent defense line ( X coordinate )
        print "wm.theirDefenseLineX()", wm.theirDefenseLineX()

        # get the opponent offense line ( X coordinate )
        print "wm.theirOffenseLineX()", wm.theirOffenseLineX()

        # get the teammate defense line ( X coordinate )
        print "wm.ourDefenseLineX()", wm.ourDefenseLineX()

        # get the teammate offense line ( X coordinate )
        print "wm.ourOffenseLineX()", wm.ourOffenseLineX()

        # get the estimated last kicker's side
        # return "left" or "right"
        print "wm.lastKickerSide()", wm.lastKickerSide()

        # check if exist kickable opponent
        # return True or False
        print "wm.existKickableOpponent()", wm.existKickableOpponent()

        # check if exist kickable teammate
        # return True or False
        print "wm.existKickableTeammate()", wm.existKickableTeammate()

        # Play mode of this cycle
        # return ↓
        # "kick_off" , "play_on" , "kick_in" , "offside" ,
        # "free_kick" , "foul_charge" , "goal" , "time_over"
        print "wm.gameMode().type()", wm.gameMode().type()

        # Update play mode (necessarily required in this loop statement)
        wm.gameMode().UpdatePlayMode()

        # Advance cycle by 1
        wm.time().addTime()
