# -*- coding: utf-8 -*-
import sys
import re
import math


class World:

    def __init__(self):
        # error process
        argvs = sys.argv
        argc = len(argvs)
        if argc != 2:
            print "file open error"
            sys.exit()

        self.rcg = []
        self.rcg.append("(show 0 ((b) 0.000 0.000")

        self.rcl_l = [[None for j in range(12)]
                      for i in range(self.fullstateTime() + 1)]
        self.rcl_r = [[None for j in range(12)]
                      for i in range(self.fullstateTime() + 1)]

        self.playmode = []

        file_name = argvs[1].split(".")[0]

        self.left_team_name = re.split(
            "_[0-9]+", re.split("[0-9]+-", file_name.split("-vs-")[0])[1])[0]
        self.right_team_name = re.split(
            "_[0-9]+", file_name.split("-vs-")[1])[0]

        self.left_team_score = int(file_name.split(
            "-vs-")[0].split(self.left_team_name + "_")[1])

        self.right_team_score = int(file_name.split(
            "-vs-")[1].split(self.right_team_name + "_")[1])

        rclfile = file_name + ".rcl"
        rcgfile = file_name + ".rcg"

        # initialize game mode
        self.game_mode = Type(self.left_team_score, self.right_team_score)

        # initialize game time
        self.game_time = GameTime(0, 6000)

        # initialize last kicker side
        self.last_kicker_side = "left"

        # file open & close
        with open(rcgfile, 'r') as rcg:
            # rcg file
            for line in rcg:
                if("show" in line and int(self.rcg[-1].split(" ")[1]) < int(line.split(" ")[1])):
                    self.rcg.append(line)
                    self.game_time.game_time += 1
                    if(int(self.rcg[-1].split(" ")[1]) == 2999):
                        self.rcg.append("(show 3000 ((b) 0.000 0.000")
                        self.game_time.game_time += 1

                elif("playmode" in line):
                    mode = line.split(" ")[2].split(")")[0]
                    cycle = int(line.split(" ")[1])
                    self.playmode.append([cycle, mode])

            self.game_time.t_over = self.time().cycle()

            # error handling
            if(self.ball() is None):
                self.game_time.t_over -= 1

            # reset cycle count
            self.time().resetTime()

        # rcl file
        with open(rclfile, 'r') as rcl:
            for line in rcl:
                if(int(line.split(',')[0]) >= 1):
                    rcl_cycle = int(line.split(',')[0])
                    if(self.left_team_name in line and not "Coach" in line):
                        rcl_unum = int(line.split(self.left_team_name)[
                                       1].split(": ")[0].split("_")[1])
                        rcl_action = line.split(self.left_team_name)[1].split(
                            ": (")[1].split(" ")[0].split(")")[0]
                        self.rcl_l[rcl_cycle][rcl_unum] = PlayerObject(
                            _unum=rcl_unum, action=rcl_action)
                    elif(self.right_team_name in line and not "Coach" in line):
                        rcl_unum = int(line.split(self.right_team_name)[
                                       1].split(": ")[0].split("_")[1])
                        rcl_action = line.split(self.right_team_name)[1].split(
                            ": (")[1].split(" ")[0].split(")")[0]
                        self.rcl_r[rcl_cycle][rcl_unum] = PlayerObject(
                            _unum=rcl_unum, action=rcl_action)
    # end constructor

    """
    @brief get teammate action
    @param unum : player unum
    @return player action or NULL
    """

    def __ourAction(self, unum, cycle = 0):

        if (cycle == 0):
            cycle = self.time().cycle()

        if(self.rcl_l[cycle][unum] is None):
            return None
        return self.rcl_l[cycle][unum].Action()

    """
    @brief get opponent action
    @param unum : player unum
    @return player action or NULL
    """

    def __theirAction(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(self.rcl_r[cycle][unum] is None):
            return None
        return self.rcl_r[cycle][unum].Action()

    """
    @brief get opponent teamname
    @return const reference to the team name string
    """

    def opponentTeamName(self):
        return self.right_team_name

    """
    @brief get our teamname
    @return const reference to the team name string
    """

    def teamName(self):
        return self.left_team_name

    """
    @brief get ball info
    @return const reference to the BallObject
    """

    def ball(self, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(len(self.rcg) <= cycle):
            return None
        ball_x = float(self.rcg[cycle].split(
            "((b) ")[1].split(" ")[0])
        ball_y = float(self.rcg[cycle].split(
            "((b) ")[1].split(" ")[1])

        return BallObject(ball_x, ball_y, 0.5)

    """
    @brief get last updated time (== current game time)
    @return const reference to the game time object
    """

    def time(self):
        return self.game_time

    """
    @brief get last time updated by fullstate
    @return const reference to the game time object
    """

    def fullstateTime(self):
        return 6000

    """
    @brief get current playmode info
    @return const reference to the GameMode object
    """

    def gameMode(self):
        # update game_mode
        self.game_mode._UpdatePlayMode(self.time().cycle(), self.playmode)
        return self.game_mode

    """
    @brief get the distance from input point to the nearest opponent
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def ourDefenseLineX(self):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        defense_line = 65535.0

        if(self.rcg[self.time().cycle()] is None):
            return defense_line

        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(defense_line > teammate[i].pos().x):
                defense_line = teammate[i].pos().x

        return defense_line

    def ourOffenseLineX(self):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        offense_line = -65535.0
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(offense_line < teammate[i].pos().x):
                offense_line = teammate[i].pos().x

        return offense_line

    def theirDefenseLineX(self):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        defense_line = -65535.0
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(defense_line < opponent[i].pos().x):
                defense_line = opponent[i].pos().x

        return defense_line

    def theirOffenseLineX(self):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        offense_line = 65535.0
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        for i in range(2, 12):
            if(offense_line > opponent[i].pos().x):
                offense_line = opponent[i].pos().x

        return offense_line

    def existKickableOpponent(self):
        dist_OppToBall = self.getDistOpponentNearestToBall(True)
        dist_MateToBall = self.getDistTeammateNearestToBall(True)
        if(dist_MateToBall > dist_OppToBall and dist_OppToBall < 1.5):
            return True
        else:
            return False

    def existKickableTeammate(self):
        dist_OppToBall = self.getDistOpponentNearestToBall(True)
        dist_MateToBall = self.getDistTeammateNearestToBall(True)
        if(dist_MateToBall < dist_OppToBall and dist_MateToBall < 1.5):
            return True
        else:
            return False

    def lastKickerSide(self):
        if(self.existKickableOpponent()):
            self.last_kicker_side = "right"
        elif(self.existKickableTeammate()):
            self.last_kicker_side = "left"
        return self.last_kicker_side

    def getDistOpponentNearestTo(self, with_goalie, point):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(opponent[i])):
                d = point.dist(opponent[i])

        return d

    """
    @brief get the distance to opponent nearest to ball wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def getDistOpponentNearestToBall(self, with_goalie):
        return self.getDistOpponentNearestTo(with_goalie, self.ball().pos())

    """
    @brief get the distance from opponent nearest to self wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched opponent. if not found, a big value is returned.
    """

    def getDistOpponentNearestToSelf(self, with_goalie):
        pass

    """
    @brief get the distance from input point to the nearest teammate
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestTo(self, with_goalie, point):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)[i].split(" ")[3]), i))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(teammate[i])):
                d = point.dist(teammate[i])

        return d

    """
    @brief get the distance to teammate nearest to ball wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestToBall(self, with_goalie):
        return self.getDistTeammateNearestTo(with_goalie, self.ball().pos())

    """
    @brief get the distance from teammate nearest to self wtth accuracy count
    @param with_goalie include goalie if true
    @return distance to the matched teammate. if not found, a big value is returned.
    """

    def getDistTeammateNearestToSelf(self, with_goalie):
        pass

    """
      @brief get opponent pointer nearest to the specified player
      @param with_goalie : bool
      @param point variable pointer to store the distance
      from retuned player to point
      @return pointer to player object
    """

    def getOpponentNearestTo(self, with_goalie, point):
        opponent = []
        opponent.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            opponent.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)
                                               [i].split(" ")[3]),
                                         i, ball_pos=self.ball().pos(), action=self.__theirAction(i)))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(opponent[i].pos())):
                d = point.dist(opponent[i].pos())
                nearest_opponent = opponent[i]

        return nearest_opponent

    def getOpponentNearestToBall(self, with_goalie):
        return self.getOpponentNearestTo(with_goalie, self.ball().pos())

    def getOpponentNearestToSelf(self, with_goalie):
        pass

    def getTeammateNearestTo(self, with_goalie, point):
        teammate = []
        teammate.append(PlayerObject(0.0, 0.0, 0))
        d = 65535.0
        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[self.time().cycle()]
        for i in range(1, 12):
            teammate.append(PlayerObject(float(re.split(pattern, match)[i].split(" ")[2]),
                                         float(re.split(pattern, match)
                                               [i].split(" ")[3]),
                                         i, ball_pos=self.ball().pos(), action=self.__ourAction(i)))

        minimum = 1 if(with_goalie) else 2
        for i in range(minimum, 12):
            if(d > point.dist(teammate[i].pos())):
                d = point.dist(teammate[i].pos())
                nearest_teammate = teammate[i]

        return nearest_teammate

    def getTeammateNearestToBall(self, with_goalie):
        return self.getTeammateNearestTo(with_goalie, self.ball().pos())

    def getOpponentNearestToSelf(self, with_goalie):
        pass

    def ourPlayer(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(unum < 1 or unum > 11):
            return None

        pattern = " \(\(l [0-9]+\) "
        match = self.rcg[cycle]
        return PlayerObject(float(re.split(pattern, match)[unum].split(" ")[2]),
                            float(re.split(pattern, match)
                                  [unum].split(" ")[3]),
                            unum, self.ball(cycle).pos(), self.__ourAction(unum, cycle))

    def theirPlayer(self, unum, cycle = 0):

        if(cycle == 0):
            cycle = self.time().cycle()

        if(unum < 1 or unum > 11):
            return None

        pattern = " \(\(r [0-9]+\) "
        match = self.rcg[cycle]
        return PlayerObject(float(re.split(pattern, match)[unum].split(" ")[2]),
                            float(re.split(pattern, match)
                                  [unum].split(" ")[3]),
                            unum, self.ball(cycle).pos(), self.__theirAction(unum, cycle))

"""
 @class Vector2D
 @brief 2d vector class

 @param float x
 @param float y
"""


class Vector2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos(self):
        return Vector2D(self.x, self.y)

    def abs(self):
        return Vector2D(abs(self.x), abs(self.y))

    def absX(self):
        return abs(self.x)

    def absY(self):
        return abs(self.y)

    def dist(self, point):
        d = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return d


"""
  @class Circle2D
  @brief 2d circle class

  @param Vector2d center
  @param float radius
"""


class Circle2D:

    def __init__(self, center_pos, radius):
        self.center_pos = center_pos
        self.radius = radius

    def center(self):
        return self.center_pos

    def contains(self, pos):
        if(self.center_pos.dist(pos) <= self.radius):
            return True
        else:
            return False

"""
  @class Line2D
  @brief 2d straight line class
  @param Vector2D pos1
  @param Vector2D pos2

  @Line Fomula: aX + bY + c = 0
"""


class Line2D:

    def __init__(self, p1, p2):
        self.a = -(p2.y - p1.y)
        self.b = p2.x - p1.x
        self.c = -self.a * p1.x - self.b * p1.y

    def dist(self, p):
        return math.fabs((self.a * p.x + self.b * p.y + self.c) / math.sqrt(self.a * self.a + self.b * self.b))

    """
      @brief get the intersection point with 'line'
      @param line considered line
      @return intersection point. if it does not exist,
      the invalidated value vector is returned.
    """

    def intersection(self, line):

        if(self.a * line.b == line.a * self.b):
            return Vector2D(-100.0, -100.0)

        intersection_x = (self.b * line.c - line.b * self.c) / \
            (self.a * line.b - line.a * self.b)
        intersection_y = (line.a * self.c - self.a * line.c) / \
            (self.a * line.b - line.a * self.b)

        if(intersection_x > 52.5000 or intersection_x < -52.5000
           or intersection_y > 34.000 or intersection_y < -34.000):
            return Vector2D(-100.0, -100.0)

        return Vector2D(intersection_x, intersection_y)

    """
      @brief check if the slope of this line is same to the slope of 'line'
      @param line considered line
      @retval true almost same
      @retval false not same
    """

    def isParallel(self, line):
        if(math.fabs(self.a * line.b - line.a * self.b) <= 0.051):
            return True
        else:
            return False

    def getA(self):
        return self.a

    def getB(self):
        return self.b

    def getC(self):
        return self.c

"""
  @class Rect2D
  @brief 2D rectangle regin class.

  The model and naming rules are depend on soccer simulator environment
          -34.0
            |
            |
-52.5 ------+------- 52.5
            |
            |
          34.0
"""


class Rect2D:

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def top(self):
        return self.top_left.y

    def bottom(self):
        return self.bottom_right.y

    def left(self):
        return self.top_left.x

    def right(self):
        return self.bottom_right.x

    def center(self):
        return Vector2D((self.left() + self.right()) * 0.5, (self.top() + self.bottom()) * 0.5)

    def contains(self, point):
        if(self.left() <= point.x and point.x <= self.right()
           and self.top() <= point.y and point.y <= self.bottom()):
            return True
        else:
            return False


class BallObject(Vector2D):

    def __init__(self, x, y, ball_size=0.5):
        Vector2D.__init__(self, x, y)
        self.ball_size = ball_size

    def size(self):
        return self.ball_size


class GameTime:

    def __init__(self, game_time, t_over):
        self.game_time = game_time
        self.t_over = t_over

    def resetTime(self):
        self.game_time = 1

    def kick_off(self):
        return 1

    def time_over(self):
        return self.t_over

    def addTime(self):
        self.game_time += 1

        if(self.game_time == 3000):
            self.game_time = 3001

    def cycle(self):
        return self.game_time

    def setCycleTo(self, c):
        if(1 <= c and c <= self.time_over):
            self.game_time = c


"""
@brief get current playmode type
@return client side playmode type Id
"""
# playmode(
#   kick_off
#   play_on
#   kick_in
#   offside
#   free_kick
#   foul_charge
#   goal
#   time_over
# )


class Type:

    def __init__(self, score_l, score_r):
        self.mode = "kick_off"
        self.score_l = score_l
        self.score_r = score_r

    def type(self):
        return self.mode

    def scoreLeft(self):
        return self.score_l

    def scoreRight(self):
        return self.score_r

    def _UpdatePlayMode(self, cycle, line):
        for i in line:
            if(i[0] <= cycle):
                self.mode = i[1]
            elif(i[0] > cycle):
                break

    def UpdatePlayMode(self):
        pass

    def __CheckPlayMode(self):
        return self.mode

    def __ChangePlayModeToFoul(self):
        self.mode = "foul_charge"

    def __ChangePlayModeToOffSide(self):
        self.mode = "offside"

    def __ChangePlayModeToPlayOn(self):
        self.mode = "play_on"

"""
@class PlayerObject
@brief observed player object class
"""


class PlayerObject(Vector2D):

    def __init__(self, x=0.0, y=0.0, _unum=0, ball_pos=Vector2D(0.0, 0.0), action="unknown"):
        Vector2D.__init__(self, x, y)
        self._unum = _unum
        self.ball_pos = ball_pos
        self.action = action

    def isKickable(self):
        if(self.pos().dist(self.ball_pos) < 1.5):
            return True
        else:
            return False

    def unum(self):
        return self._unum

    def distFromBall(self):
        return self.pos().dist(self.ball_pos)

    def Action(self):
        return self.action
