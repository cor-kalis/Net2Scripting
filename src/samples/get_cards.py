"""
Sample script to fetch all cards
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
        # Obtain all Net2 cards
        print(Net2XS.dataset_to_str(net2.get_cards()))
