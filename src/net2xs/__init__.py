"""
The module that offers access to the Paxton Net2 server
"""
import clr
import os
import sys

import settings
from net2xs.conversions import date_time_to_net, flex_date_time_to_net, \
    time_zones_to_py, access_levels_to_py, access_level_detail_to_py
from datetime import datetime
from net2base import Net2Base
from pylog4net import Log4Net
from threading import RLock
from System import Array
from System.Data import DataSet
from System.Reflection import Assembly

# Minimal required net2 version
MIN_NET2_VERSION = 501
# Paxton assembly
PAXTON_ASSEMBLY = 'Paxton.Net2.OEMClientLibrary'


def readable_min_version():
    """Show a user readable minimum version
    """
    major = MIN_NET2_VERSION / 100
    minor = MIN_NET2_VERSION - major * 100
    return "%d.%d" % (major, minor)


class Net2XSException(Exception):
    """Exception class for net2 xs
    """
    pass


# The code below is required to determine if the already installed
# Net2 version can be used, or that the packaged version is required.
try:
    # Obtain paxton assembly reference
    asm = Assembly.LoadWithPartialName(PAXTON_ASSEMBLY)

    # Found: check the version
    if asm:
        ver = asm.GetName().Version
        if ver.Major * 100 + ver.Minor < MIN_NET2_VERSION:
            raise Net2XSException(
                'Only Net2 V%s or higher is supported' %
                readable_min_version())

    # Not found: enable the packaged paxton libs
    else:
        # Add path lib path to search path
        PAXTON_LIB_DIR = os.path.join(settings.LIB_DIR, 'paxton')
        if PAXTON_LIB_DIR not in sys.path:
            sys.path.append(PAXTON_LIB_DIR)

    try:
        Assembly.LoadWithPartialName(PAXTON_ASSEMBLY)
        clr.AddReference(PAXTON_ASSEMBLY)
        from Paxton.Net2.OemClientLibrary import OemClient as OC
        from Paxton.Net2.OemClientLibrary import AccessLevelDetailSet
        from Paxton.Net2.OemClientLibrary import TimezonesSet
        from Paxton.Net2.OemClientLibrary import EventViewEnums
    except:
        raise Net2XSException('Failed to load the library')

except Exception as e:
    Log4Net.get_logger('Net2XS').Fatal('Paxton error: %s' % str(e))
    sys.exit(1)
# end of paxton loading


class Net2XS(Net2Base):
    """Net2 Access class
    """

    # Class variables
    _logger = Log4Net.get_logger('Net2XS')
    _lock = RLock()

    def __init__(self, host='localhost', port=8025):
        """Class constructor
        """
        self._client = None
        self._host = host
        self._port = port
        self._connected = False
        self._on_acu_event = None

    def __enter__(self):
        """With enter handler
        """
        return self

    def __exit__(self, type, value, traceback):
        """With exit handler
        """
        self.dispose()

    def _check_client(self):
        """Check is client connection is valid
        """
        if not self._client or not self._connected:
            raise Net2XSException('Not connected')

    def authenticate(self, user_id, password):
        """Authenticate to Net2
        """
        with Net2XS._lock:
            # Save for re authentication
            self._user_id = user_id
            self._password = password

            self.dispose()

            Net2XS._logger.Debug('Connecting to net2 server on %s:%d' %
                                 (self._host, self._port))
            self._client = OC(self._host, self._port)
            methods = self._client.AuthenticateUser(user_id, password)
            if not methods:
                raise Net2XSException('Authentication failed: ' +
                                      self._client.LastErrorMessage)
            else:
                self._connected = True

            # Add disconnect reconnect handlers
            self._client.Net2ServerReconnected += (
                OC.Net2ServerReconnectedHandler(self._reconnected))
            self._client.Net2ServerDisconnected += (
                OC.Net2ServerDisconnectedHandler(self._disconnected))

            # Add acu event handler
            self._client.Net2AccessEvent += (
                OC.Net2AcuEventHandler(self._acu_event))

            Net2XS._logger.Debug('Authenticated')

    @property
    def client_version(self):
        """Client version
        """
        asm = Assembly.GetAssembly(OC)
        ver = asm.GetName().Version
        return (ver.Major, ver.Minor)

    def query_db(self, query):
        """Perform a db query

        Returns a dataset
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.QueryDb(query)

    def are_doors_being_synchronised(self):
        """Return if synchronization is taking place

        Returns a boolean
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.AreDoorsBeingSynchronised()

    def get_doors(self, device_address=-1):
        """Get all doors (ViewDoors)

        Device_address is an optional integer
        Returns a dataset
        """
        with Net2XS._lock:
            self._check_client()
            if device_address < 0:
                return self._client.ViewDoors().DoorsDataSource
            else:
                return self._client.ViewDoors(device_address).DoorsDataSource

    def get_door_name(self, device_address):
        """Obtain door name

        Returns a string
        """
        with Net2XS._lock:
            self._check_client()
            dataset = self._client.ViewDoors(device_address).DoorsDataSource
            if (not dataset or
                    dataset.Tables.Count < 1 or
                    dataset.Tables[0].Rows.Count == 0):
                return None
            return dataset.Tables[0].Rows[0].Name

    def get_departments(self):
        """Get all departments (ViewDepartments)

        Returns a dataset
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.ViewDepartments().DepartmentsDataSource

    def close_door(self, device_address):
        """Close a door

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.CloseDoor(device_address)

    def hold_door_open(self, device_address):
        """Hold a door open

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.HoldDoorOpen(device_address)

    def control_door(self, device_address, relay, function, door_open_time, led_flash):
        """Control a door

        Relay is 0 or 1, for relay 1 or 2.
        Function 0 Close, 1 Timed open, 2 Hold Open.
        Door_open_time in ms.
        Led_flash see Net2 API.
        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.ControlDoorEx(
                device_address, relay, function, door_open_time, led_flash)

    def get_department_name(self, department_id):
        """Get department name by id

        Returns a string or None if department was not found
        """
        dataset = self.query_db(
            'select DepartmentName from sdk.Departments'
            ' where DepartmentID=%d' % department_id)
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count == 0):
            return None
        return dataset.Tables[0].Rows[0][0]

    def get_users_ex(self, name=None):
        """Get users, from the UsersEx view.

        Name param is optional tuple (first_name, sur_name)
        Returns a dataset
        """
        query = 'select * from sdk.UsersEx'
        if name and len(name) == 2:
            first_name, sur_name = name
            query = ("%s where FirstName='%s' and Surname='%s'" %
                     (query, first_name, sur_name))
        return self.query_db(query)

    def get_user_id_by_name(self, name):
        """Get user id by name

        Name is a (first_name, sur_name) tuple
        Returns the id or -1 if not found.
        """

        dataset = self.get_users(name)
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count == 0):
            return -1
        return dataset.Tables[0].Rows[0].get_Item("UserID")

    def get_users(self, name=None):
        """Get users, from the ViewUserRecords call

        Name param is optional tuple (first_name, sur_name)
        Returns a dataset
        """
        with Net2XS._lock:
            self._check_client()
            wheres = ['Active=1']
            if name and len(name) == 2:
                first_name, sur_name = name
                if first_name:
                    wheres.append("FirstName='%s'" % first_name)
                if sur_name:
                    wheres.append("Surname='%s'" % sur_name)

            return self._client.ViewUserRecords(
                ' and '.join(wheres)).UsersDataSource

    def get_user_record(self, user_id):
        """Get user record, from the ViewUserRecords call

        Returns an IUserView user record or None if not found
        """
        with Net2XS._lock:
            self._check_client()

            # Fetch current user info
            users = self._client.ViewUserRecords(
                'UserID=%d' % user_id).UsersList()

            if users.Count != 1 or not users.ContainsKey(user_id):
                return None

            return users[user_id]

    def get_user_name(self, user_id):
        """Get user name

        Returns a string or None when user is not found
        """
        dataset = self.query_db(
            'select Username from sdk.UsersEx where UserID=%d' % user_id)
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count == 0):
            return None
        return dataset.Tables[0].Rows[0][0]

    def add_user(
            self,
            access_level_id=1,
            department_id=0,
            anti_passback_ind=False,
            alarm_user_ind=False,
            first_name=None,
            middle_name=None,
            sur_name=None,
            telephone_no=None,
            telephone_extension=None,
            pin_code=None,
            activation_date=None,
            active=True,
            fax_no=None,
            expiry_date=None,
            custom_fields=None,
            user_picture=None):
        """Add user record

        DateTime fields can be either python or dotnet objects.
        If activation date is None, the current date will be used.
        If expiry date is None, the user entry will not expire.
        Custom_fields is a string array (15) of which the first element is
        ignored.
        Returns True on success.
        """

        # If no user name is given at all: create one (required by Net2)
        if not first_name and not sur_name and not middle_name:
            first_name = "New"
            sur_name = "User"

        with Net2XS._lock:
            self._check_client()
            return self._client.AddUserRecord(
                access_level_id,
                department_id,
                anti_passback_ind,
                alarm_user_ind,
                first_name,
                middle_name,
                sur_name,
                telephone_no,
                telephone_extension,
                pin_code,
                None,
                flex_date_time_to_net(activation_date) or self.now_date,
                0,
                0,
                active,
                fax_no,
                flex_date_time_to_net(expiry_date) or self.no_expiration_date,
                custom_fields,
                user_picture)

    def modify_user(
            self,
            user_id,
            access_level_id=None,
            department_id=None,
            anti_passback_ind=None,
            alarm_user_ind=None,
            first_name=None,
            middle_name=None,
            sur_name=None,
            telephone_no=None,
            telephone_extension=None,
            pin_code=None,
            activation_date=None,
            active=None,
            fax_no=None,
            expiry_date=None,
            custom_fields=None,
            user_picture=None,
            delete_image=False):
        """Modify user record

        Fields omitted keep their original value.
        Custom_fields is a string array (15) of which the first element is
        ignored.
        Providing None custom values in the array, leaves the original value
        unchanged.
        Returns True on success.
        """
        # Fetch current user info
        uview = self.get_user_record(user_id)
        if not uview:
            return False

        with Net2XS._lock:
            self._check_client()
            return self._client.UpdateUserRecord(
                user_id,
                uview.AccessLevelId if access_level_id is None else access_level_id,
                uview.DepartmentId if department_id is None else department_id,
                uview.AntiPassbackUser if anti_passback_ind is None else anti_passback_ind,
                uview.AlarmUser if alarm_user_ind is None else alarm_user_ind,
                first_name,
                middle_name,
                sur_name,
                telephone_no,
                telephone_extension,
                pin_code,
                None,
                flex_date_time_to_net(activation_date) or uview.ActivationDate,
                uview.Active if active is None else active,
                fax_no,
                flex_date_time_to_net(expiry_date) or uview.ExpiryDate,
                custom_fields,
                user_picture,
                delete_image)

    def delete_user(self, user_id):
        """Delete user record

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.PurgeUser(user_id)

    def deactivate_user(self, user_id):
        """Deactivate user. Preferred method iso delete.

        Returns True on success
        """
        return self.modify_user(
            user_id=user_id,
            access_level_id=0,
            department_id=0,
            pin_code="",
            active=False)

    def modify_user_access_level(self, user_id, access_level_id):
        """Alter user access level

        Returns True on success
        """
        return self.modify_user(
            user_id=user_id,
            access_level_id=access_level_id)

    def modify_user_picture(self, user_id, user_picture):
        """Alter user picture. If user_picture is None, remove the picture.

        Returns True on success
        """
        return self.modify_user(
            user_id=user_id,
            user_picture=user_picture,
            delete_image=True if not user_picture else False)

    def get_area_ids(self, device_address):
        """Get area ids of a device

        Returns a tuple with area id's (in, out)
        """
        dataset = self.query_db(
            'select b.ToAreaID from sdk.PeripheralNames a'
            ' inner join sdk.AreaGateways b on'
            ' a.PeripheralID=b.PeripheralID and'
            ' a.SerialNumber=%d order by a.SubAddress' %
            (device_address))
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count != 2):
            return None
        return (dataset.Tables[0].Rows[0][0], dataset.Tables[0].Rows[1][0])

    def get_device_addr_info(self):
        """Obtain all relevant device address info

        Returns a dataset
        """
        return self.query_db(
            'select a.SerialNumber, a.SubAddress, a.PeripheralID, b.ToAreaID'
            ' from sdk.PeripheralNames a'
            ' inner join AreaGateways b on a.PeripheralID=b.PeripheralID'
            ' order by a.SerialNumber')

    def get_time_slots(self, access_level_id, area_id):
        """Obtain allocated timeslots

        Returns a dataset
        """
        return self.query_db(
            'select * from sdk.Timeslots'
            ' where TimezoneID='
            '(select TimezoneID from AccessLevelMembers'
            ' where AccessLevelID=%d and AreaID=%d)' %
            (access_level_id, area_id or -1))

    def get_time_zones(self, time_zone_id=-1):
        """Obtain timezones, including slot data

        Time_zone_id is optional. If not provided, all timezones are returned.
        Returns a dataset
        """
        with Net2XS._lock:
            self._check_client()
            if time_zone_id < 0:
                return self._client.ViewTimezones().TimezonesDataSource
            else:
                return self._client.ViewTimezones(
                    time_zone_id, False).TimezonesDataSource

    def get_py_time_zones(self, time_zone_id=-1):
        """Like get_time_zones, but returns a python array of TimeZone objects

        Returns an array of TimeZone objects
        """
        dataset = self.get_time_zones(time_zone_id)
        return time_zones_to_py(dataset)

    def add_time_zone(self, time_zone):
        """Add new time zone

        Time_zone is a python TimeZone object type.
        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            tz_set = TimezonesSet()
            for slot in time_zone.slots:
                tz_set.Tables[1].AddTimeslotsRow(
                    slot.id,
                    time_zone.id,
                    date_time_to_net(slot.start_time),
                    date_time_to_net(slot.end_time),
                    slot.day)

            # To array
            ts_array = Array[TimezonesSet.TimeslotsRow](
                len(time_zone.slots) * [None])
            for i, row in enumerate(tz_set.Tables[1].Rows):
                ts_array[i] = row

            # Dispose timezones set
            tz_set.Dispose()

            return self._client.AddTimezone(time_zone.name, ts_array)

    def delete_time_zone(self, time_zone_id):
        """Remove time zone with given id

        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.DeleteTimezone(time_zone_id)

    def update_time_zone(self, time_zone):
        """Update existing time zone

        Time_zone is a python TimeZone object type.
        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            tz_set = TimezonesSet()
            nr_slots = len(time_zone.slots)

            if nr_slots:
                for slot in time_zone.slots:
                    tz_set.Tables[1].AddTimeslotsRow(
                        slot.id,
                        time_zone.id,
                        date_time_to_net(slot.start_time),
                        date_time_to_net(slot.end_time),
                        slot.day)

            # Work around for bug "Update Timezone with empty timeslot" (forum)
            # At least 1 row is required for the update to work correctly.
            # Should be fixed in V4.21
            # TODO: only perform for lower versions?
            else:
                nr_slots = 1
                tz_set.Tables[1].AddTimeslotsRow(
                    -1,
                    time_zone.id,
                    date_time_to_net(datetime(1899, 12, 30, 23, 59, 59)),
                    date_time_to_net(datetime(1899, 12, 30, 23, 59, 59)),
                    0)

            # To array (bit awkward in Python.Net)
            ts_array = Array[TimezonesSet.TimeslotsRow](nr_slots * [None])
            for i, row in enumerate(tz_set.Tables[1].Rows):
                ts_array[i] = row

            # Dispose timezones set
            tz_set.Dispose()

            return self._client.UpdateTimezone(time_zone.id, ts_array)

    def get_time_zone_id_by_name(self, name):
        """Get time zone id of time zone with given name

        Returns a string or None when the timezone could not be found.
        """
        dataset = self.query_db(
            "select TimezoneID from sdk.Timezones"
            " where Name='%s'" % name)
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count == 0):
            return None
        return dataset.Tables[0].Rows[0][0]

    def get_access_levels(self, prefix=None):
        """Obtain access levels, optinally profiding a name prefix filter

        Prefix is an optional parameter to obtain only access levels with the
        given prefix.
        Details need to be fetched separately.
        Returns a dataset.
        """
        query = 'select * from sdk.AccessLevels'
        if prefix:
            query = "%s where AccessLevelName like '%s%%'" % (query, prefix)
        return self.query_db(query)

    def get_access_level_details(self, access_level_id):
        """Obtain access level details

        Returns a dataset.
        """
        query = 'select * from sdk.AccessLevelMembers where AccessLevelID=%d' % (access_level_id)
        return self.query_db(query)

    def get_py_access_levels(self, prefix=None):
        """Like get_access_level, but returning a python array of AccessLevel
        objects including details!

        Returns an array of AccessLevel objects.
        """
        dataset = self.get_access_levels(prefix)
        if not dataset:
            return []
        access_levels = access_levels_to_py(dataset)
        for al in access_levels:
            dataset = self.get_access_level_details(al.id)
            if dataset:
                access_level_detail_to_py(al, dataset)

        return access_levels

    def add_access_level(self, access_level):
        """Add new access level

        Access_level is a python AccessLevel object type.
        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            detail_set = AccessLevelDetailSet()
            if access_level.details:
                for detail in access_level.details:
                    detail_set.Tables[0].AddAccessLevelDetailRow(
                        None,
                        detail[0],  # time zone id
                        None,
                        detail[1],  # area id
                        None,
                        -1,  # address
                        -1,  # sub address
                        -1)  # access level id

            return self._client.AddAccessLevel(access_level.name, detail_set)

    def delete_access_level(self, access_level_id):
        """Delete access level

        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.DeleteAccessLevel(access_level_id)

    def update_access_level(self, access_level):
        """Update access level

        Access_level is a python AccessLevel object type.
        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()

            if access_level.details:
                detail_set = AccessLevelDetailSet()
                for detail in access_level.details:
                    detail_set.Tables[0].AddAccessLevelDetailRow(
                        None,
                        detail[0],  # time zone id
                        None,
                        detail[1],  # area id
                        None,
                        -1,  # address
                        -1,  # sub address
                        -1)  # access level id

            # Work around for similar bug as with the time zone slots
            # When details are empty, existing data will not be cleared
            # Therefore set TimezoneID to 0 for any existing entries
            else:
                ald = self._client.ViewAccessLevelDetail(access_level.id)
                detail_set = ald.AccessLevelDetailsDataSource
                for row in detail_set.Tables[0].Rows:
                    row.TimezoneID = 0

            return self._client.UpdateAccessLevel(
                access_level.id, access_level.name, detail_set)

    def get_access_level_id_by_user(self, user_id):
        """Get access level id of given user

        Returns an integer or None if the user could not be found
        """
        with Net2XS._lock:
            self._check_client()
            dataset = self._client.ViewUserRecords(
                'UserID=%d' % (user_id)).UsersDataSource
            if (not dataset or
                    dataset.Tables.Count < 1 or
                    dataset.Tables[0].Rows.Count == 0):
                return None
            return dataset.Tables[0].Rows[0].AccessLevelID

    def get_access_level_id_by_name(self, name):
        """Get access level id of level with given name

        Returns a string or None if the accesslevel could not be found.
        """
        dataset = self.query_db(
            "select AccessLevelID from sdk.AccessLevels"
            " where AccessLevelName='%s'" % name)
        if (not dataset or
                dataset.Tables.Count < 1 or
                dataset.Tables[0].Rows.Count == 0):
            return None
        return dataset.Tables[0].Rows[0][0]

    def get_operator_level(self, user_id):
        """Get operator level of the given user id

        Returns an integer.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.GetOperatorLevel(user_id)

    def add_card(self, card_nr, type_id, user_id):
        """Add a new card to the given user

        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.AddCard(card_nr, type_id, user_id)

    def delete_card(self, card_nr):
        """Delete a card with the given card_nr

        Returns True on success (even if card_nr did not exist).
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.DeleteCard(card_nr)

    def get_cards(self, user_id=None):
        """Obtain all 'cards' of the given user id

        If no user_id is given, all cards are returned.
        Returns a dataset.
        """
        with Net2XS._lock:
            self._check_client()
            # Setup dataset to return
            dataset = DataSet()
            table = dataset.Tables.Add()
            table.Columns.Add("UserID")
            table.Columns.Add("CardNumber")
            table.Columns.Add("LostCard")
            table.Columns.Add("CardTypeID")

            # Fetch normal cards
            query = ("select * from sdk.Cards" +
                     " where CardTypeID is not null" +
                     " and CardTypeID <> 7" +
                     " and CardNumber <> 100000000 + UserID")
            if type(user_id) is int:
                query += " and UserID=%d" % (user_id)
            card_dataset = self.query_db(query)
            if card_dataset and card_dataset.Tables.Count > 0:
                for row in card_dataset.Tables[0].Rows:
                    table.Rows.Add(row['UserID'],
                                   row['CardNumber'],
                                   row['LostCard'],
                                   row['CardTypeID'])

            # Fetch vehicle registrations
            query = "select * from sdk.UserVehicleIndex"
            if type(user_id) is int:
                query += " where UserID=%d" % (user_id)
            vehicle_dataset = self.query_db(query)
            if vehicle_dataset and vehicle_dataset.Tables.Count > 0:
                for row in vehicle_dataset.Tables[0].Rows:
                    table.Rows.Add(row['UserID'],
                                   row['VehicleIndex'],
                                   False,
                                   7)
            return dataset

    def add_event_record(
            self,
            #CK: check!
            #event_type, event_subtype=EventViewEnums.Net2EventSubTypes.None,
            event_type, event_subtype=None,
            address=0, subaddress=0, user_id=None, card_nr=0,
            event_detail=None,
            linked_event_id=0, ioboard_id=0, input_id=0, output_id=0):
        """Add an event record

        Returns True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.AddEventRecord(
                event_type,
                event_subtype,
                address, subaddress, user_id, card_nr, event_detail,
                linked_event_id, ioboard_id, input_id, output_id)

    def add_acu(self, address, acu_type):
        """Add new acu device

        Acu_types: Classic = 1, Nano = 2, Plus = 3, EasyProxNano = 4, PaxLoc = 7, PaxLocMifare = 8
        Returns True on success. (up till 4.27, there is a bug in the SDK causing a False on success)
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.AddACU(address, acu_type)

    def delete_acu(self, address):
        """Delete acu device

        Return True on success.
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.DeleteACU(address)

    @property
    def last_error_message(self):
        """Last error message
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.LastErrorMessage

    @property
    def no_expiration_date(self):
        """The 'special' no expiration date of Net2 (1753-01-01)

        Returns dotnet DateTime object
        """
        return date_time_to_net(datetime(year=1753, month=1, day=1))

    @property
    def now_date(self):
        """The now datetime

        Returns dotnet DateTime object
        """
        return date_time_to_net(datetime.now())

    def dispose(self):
        """Dispose Net2 client
        """
        with Net2XS._lock:
            if self._client:
                try:
                    self._client.Dispose()
                    self._client = None
                    Net2XS._logger.Debug('Disposed')
                except:
                    pass

    def _reconnected(self, sender, event_args):
        """Reconnect handler
        """
        if event_args.ReAuthenticationRequired:
            try:
                self.authenticate(self._user_id, self._password)
                self._connected = True
                Net2XS._logger.Debug('Reconnected')
            except Exception as e:
                Net2XS._logger.Debug('Reconnect error: %s' % str(e))
        else:
            self._connected = True

    def _disconnected(self, sender, event_args):
        """Disconnect handler
        """
        Net2XS._logger.Debug('Disconnected')
        self._connected = False

    @property
    def on_acu_event(self):
        return self._on_acu_event

    @on_acu_event.setter
    def on_acu_event(self, value):
        self._on_acu_event = value

    def _acu_event(self, sender, event_view):
        """Acu event handler
        """
        if self.on_acu_event:
            try:
                self.on_acu_event(sender, event_view)
            except Exception as e:
                Net2XS._logger.Debug('Acu even handler error: %s' % str(e))

    def monitor_acu(self, address):
        """Monitor events of given acu

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.MonitorAcu(address)

    def stop_monitoring_acu(self, address):
        """Stop monitoring events of given acu

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.StopMonitoringAcu(address)

    def activate_ioboard_relays(self, ioboard_id, settings):
        """Control ioboard relays

        Returns True on success
        """
        with Net2XS._lock:
            self._check_client()
            return self._client.ActivateIoBoardRelays(
                ioboard_id, settings)

    @classmethod
    def door_status_str(cls, status):
        """Translate door status to human readable string

        Returns a csv string with the combined status bits.
        """
        ret = []
        if status & OC.DoorStatusFlags.PSUIsOK:
            ret.append('psu ok')
            if status & OC.DoorStatusFlags.IntruderAlarm:
                ret.append('intruder')
            if not status & OC.DoorStatusFlags.TamperStatusGood:
                ret.append('tampered')
            if status & OC.DoorStatusFlags.DoorContactClosed:
                ret.append('door contact closed')
            if status & OC.DoorStatusFlags.AlarmTripped:
                ret.append('alarm')
            if status & OC.DoorStatusFlags.DoorOpen:
                ret.append('door open')
        # When psu not ok, other state bits are irrelevant
        else:
            ret.append('psu not ok')
        return ', '.join(ret)
