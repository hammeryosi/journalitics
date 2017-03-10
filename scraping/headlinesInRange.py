import common
import sys
args = sys.argv
common.headLinesInRange(args[1], args[2],
                        args[3], saveTo=args[4])