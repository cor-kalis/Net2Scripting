"""
Sample script to hold all known doors open for a few seconds.
Also shows how to use the logger function.
"""
import time
from Net2Scripting import init_logging
from Net2Scripting.net2xs import Net2XS
from Net2Scripting.pylog4net import Log4Net

# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"


def get_doors(net2):
    """Obtain a list of all known doors
    """
    res = []
    dataset = net2.get_doors()
    if dataset and dataset.Tables.Count > 0:
        for row in dataset.Tables[0].Rows:
            res.append(row.Address)
    return res


if __name__ == "__main__":

    # Init log4net
    init_logging()

    # Create logger object
    logger = Log4Net.get_logger('open_all_doors')

    with Net2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)
        # Get list off door addresses
        doors = get_doors(net2)
        # Open each door
        for door in doors:
            if not net2.hold_door_open(door):
                logger.Error(
                    "Failed to hold door %d open: %s." %
                    (door, net2.last_error_message))
            else:
                logger.Info("Set door %d open." % (door))

        logger.Info("Now all doors are open...")
        time.sleep(3)

        # Close each door
        for door in doors:
            if not net2.close_door(door):
                logger.Error(
                    "Failed to close door %d: %s." %
                    (door, net2.last_error_message))
            else:
                logger.Info("Set door %d closed." % (door))

        logger.Info("Now all doors are closed again")
