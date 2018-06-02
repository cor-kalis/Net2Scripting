"""
Sample script to add many users with cards
"""
from net2xs import Net2XS

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

        # Add 1000 users
        for i in range(1, 1001):
            first_name = "Test"
            sur_name = "User #%04d" % (i)
            card_nr = 77770000 + i

            # Add user
            res = net2.add_user(
                first_name=first_name,
                sur_name=sur_name)
            if not res:
                print("Failed to add user %s %s: %s" %
                      (first_name, sur_name, net2.last_error_message))
                continue

            # Get user id
            user_id = net2.get_user_id_by_name((first_name, sur_name))
            if user_id < 0:
                print("Failed to find user %s %s" % (first_name, sur_name))
                continue

            # Create card
            res = net2.add_card(card_nr, 1, user_id)
            if not res:
                print("Failed to add card to user %s %s: %s" %
                      (first_name, sur_name, net2.last_error_message))
