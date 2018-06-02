"""
Sample script to add a new user
"""

from Net2Scripting import init_logging
from Net2Scripting.net2xs import Net2XS

# Uncomment to use dotnet DateTime objects
# from System import DateTime

# Uncomment to use python datetime objects
# from datetime import datetime


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
        # Add new user
        res = net2.add_user(
            access_level_id=1,  # Always, all doors
            department_id=0,  # No department
            anti_passback_ind=False,
            alarm_user_ind=False,
            first_name="John",
            middle_name=None,
            sur_name="Doe",
            telephone_no="12345678",
            telephone_extension=None,
            pin_code=None,
            activation_date=None,  # Now
            # Or supply a dotnet DateTime object (also see import)
            # activation_date=DateTime(2018, 1, 2),
            # Or supply a python datetime object (also see import)
            # activation_date=datetime(2018, 1, 2),
            active=True,
            fax_no=None,
            expiry_date=None)  # Never expire (also see activation_date)

        if res:
            print("Success")
        else:
            print("Failure")
