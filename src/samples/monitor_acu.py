"""
Sample script to monitor acu
"""

from time import sleep
from net2xs import Net2XS


# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"
# Acu to monitor
ACU_ADDRESS = 1219195


def handle_acu_event(sender, event_view):
    """Handler for ACU event
    """
    print("-----------------------")
    print("address=", event_view.Address)
    print("card=", event_view.CardNumber)
    print("department=", event_view.Department)
    print("userid=", event_view.UserId)


if __name__ == "__main__":

    with Net2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)

        # Set function to handle ACU event
        net2.on_acu_event = handle_acu_event

        res = net2.monitor_acu(ACU_ADDRESS)
        if not res:
            print("Failed to monitor ACU %d" % (ACU_ADDRESS))
        else:
            print("Monitoring ACU %d; press <ctrl>C to quit" % (ACU_ADDRESS))
            while True:
                try:
                    sleep(1)
                except KeyboardInterrupt:
                    break
            net2.stop_monitoring_acu(ACU_ADDRESS)
