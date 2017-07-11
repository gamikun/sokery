import signal
import socket
import argparse
import time


class Global:
    run = True

parser = argparse.ArgumentParser()
parser.add_argument('host', nargs=1)
parser.add_argument('port', nargs=1, type=int)
parser.add_argument('-p', dest='payload', type=str, default='hello')
parser.add_argument('-t', dest='tick', type=float, default=2.0)
parser.add_argument('--br', dest='line_break', default=False,
                            action='store_const', const=True)
args = parser.parse_args()
address = (args.host[0], args.port[0], )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

while Global.run:
    try:
        s.send(args.payload)
        if args.line_break:
            s.send('\n')
        print('sending: {}'.format(args.payload))
        time.sleep(args.tick)

    except KeyboardInterrupt:
        break

    except socket.error as ex:
        print(ex)
        break