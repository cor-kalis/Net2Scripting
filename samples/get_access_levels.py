"""
Sample script to fetch all access levels
"""

from Net2Scripting import init_logging
from Net2Scripting.net2xs import Net2XS

# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"


if __name__ == "__main__":

    # Init log4net
    init_logging()

    with Net2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)
        # Show all access levels and their details
        for al in net2.get_py_access_levels():
            print(al)
