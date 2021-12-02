from naoqi import ALProxy
import time
import os
from search import generate_transition, mandatory
from pygame import mixer


def main(ip, port, mandatory):
    starting_time = time.time()

    play_song()

    do_move(mandatory[0], ip, port)
    past_moves = [mandatory[0]]

    # starting iteration trough mandatory positions
    for i in range(1, len(mandatory)):

        # creating a subsequence
        subsequence = generate_transition(past_moves)
        for j in subsequence:
            # for each move (not including the first one) a check on its state will be performed, in
            # order to understand if NAO is sitting or standing
            check_precondition(j, ip, port)
            past_moves.append(j)
        check_precondition(mandatory[i], ip, port)
        past_moves.append(mandatory[i])
    mixer.music.stop()
    tot = time.time() - starting_time
    s = 0
    past_names = []

    for i in past_moves:
        s += i.t
        past_names.append((i.__name__, i.t))
    print past_names
    print 'total time: ', s
    print 'actual time: ', tot


def play_song():
    mixer.init()
    mixer.music.load('/home/nao/PycharmProjects/NAO-PROJECT/all_star.mp3')
    mixer.music.play()


# this function has been created to avoid a problem that presented itself during the execution of the moves:
# while executing, if NAO was standing and the next move was one which involved sitting, it just sat instantly,
# without the necessary animation (the opposite, if sitting and received a standing move, NAO just popped up)
def check_precondition(curr_move, ip, port):
    # if the move's pre-condition is True (NAO needs to be standing to perform it), stand up (NAO does
    # the standing animation only if it is sitting, if it is already standing it does nothing)
    if curr_move.pre:
        comm = "python2 /home/nao/PycharmProjects/NAO-PROJECT/moves/stand-command.py  {} {}".format(
            ip, port)

    # this is the opposite
    else:
        comm = "python2 /home/nao/PycharmProjects/NAO-PROJECT/moves/sit-command.py  {} {}".format(
            ip, port)
    os.system(comm)
    # after standing up or sitting down, do the move
    do_move(curr_move, ip, port)


def do_move(move, ip, port):
    try:
        motion = ALProxy("ALMotion", ip, port)
        motion.angleInterpolation(move.names, move.keys, move.times, True)
    except BaseException, err:
        print err


'''port changes everytime choreogrphe is opened, please insert correct port '''

main("127.0.0.1", 37853, mandatory)
