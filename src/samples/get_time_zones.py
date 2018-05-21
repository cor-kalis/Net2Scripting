"""
Sample script to fetch all time zones
"""

from net2xs import Net2XS

# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"


if __name__ == "__main__":

    with Net2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)
        # Show all time zones and their details
        for tz in net2.get_py_time_zones():
            print(tz)
