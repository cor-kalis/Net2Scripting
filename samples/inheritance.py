"""
Sample script to demonstrate inheritance
"""

from Net2Scripting import init_logging
from Net2Scripting.net2xs import Net2XS

# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"


class MyNet2XS(Net2XS):
    """Inherited class for additional functionality
    """
    global Net2XS

    def get_current_user_id(self):
        """Return logged on user id
        """
        # Place a lock, for thread safety
        # (if you don't have threads you kan skip this)
        with Net2XS._lock:
            # Basic check if client connection is valid
            self._check_client()
            return self._client.CurrentUserID

    def get_client_members(self):
        """Return all Net2 client object members using the introspective
        Python dir function
        """
        with Net2XS._lock:
            self._check_client()
            return dir(self._client)


if __name__ == "__main__":

    # Init log4net
    init_logging()

    with MyNet2XS(NET2_SERVER) as net2:
        # Authenticate
        net2.authenticate(OPERATOR_ID, OPERATOR_PWD)
        # Show current user id
        print("Current used id:", net2.get_current_user_id())
        # Show all members
        print("Net2 client members:", net2.get_client_members())
