"""
Sample script to modify a user.
It assumes that a John Doe user exists (see add_user sample).
"""

from net2xs import Net2XS
from datetime import datetime


# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"

# First name
FIRST_NAME = "John"
# Surname
SUR_NAME = "Doe"


if __name__ == "__main__":

    with Net2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)

        # Get user id
        user_id = net2.get_user_id_by_name((FIRST_NAME, SUR_NAME))

        print("Found user id %d" % (user_id))

        # Found a valid user id
        if user_id >= 0:

            # Modify expiration date
            res = net2.modify_user(
                user_id=user_id,
                expiry_date=datetime(2022, 12, 31))

            if res:
                print("Success")
            else:
                print("Failure")

        else:
            print("Failed to find user %s %s" % (FIRST_NAME, SUR_NAME))
