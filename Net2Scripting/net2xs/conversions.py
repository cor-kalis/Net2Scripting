"""
Module holding conversion definitions
"""
from datetime import datetime
from System import DateTime
from . deftypes import TimeZone, TimeSlot, AccessLevel


def date_time_to_py(val):
    """Convert dotnet date time format to python presentation

    Returns python datetime object.
    """
    return datetime(
        year=val.Year, month=val.Month, day=val.Day,
        hour=val.Hour, minute=val.Minute, second=val.Second)


def date_time_to_net(val):
    """Convert python to dotnet date time presentation

    Returns dotnet DateTime object.
    """
    return DateTime(
        val.year, val.month, val.day,
        val.hour, val.minute, val.second)


def flex_date_time_to_net(val):
    """Convert python to dotnet date time presentation when required

    Returns dotnet DateTime object or None.
    """
    if val is None:
        return val

    if type(val) is datetime:
        return date_time_to_net(val)

    if not type(val) is DateTime:
        raise TypeError(
            ("The time value supplied (%s), " +
             "can not be interpreted as a dotnet DateTime object") %
            (str(val)))
    return val


def time_zones_to_py(dataset):
    """Convert Net2 time zones dataset to a python presentation

    Returns array of TimeZone objects.
    """
    if not dataset or dataset.Tables.Count != 2:
        raise Exception('Timezone dataset is invalid')

    result = []

    for tz_row in dataset.Tables[0].Rows:
        time_zone = TimeZone(
            id=tz_row.TimezoneID,
            name=tz_row.Name)

        ts_rows = dataset.Tables[1].Select('TimezoneID=%d' % time_zone.id)
        for ts_row in ts_rows:
            time_slot = TimeSlot(
                id=ts_row.SlotID,
                day=ts_row.Day,
                start_time=date_time_to_py(ts_row.StartTime),
                end_time=date_time_to_py(ts_row.EndTime))
            time_zone.slots.append(time_slot)

        result.append(time_zone)
    return result


def access_levels_to_py(dataset):
    """Convert Net2 access_level dataset to a python presentation

    Returns array of AccessLevel objects.
    """
    if not dataset or dataset.Tables.Count != 1:
        raise Exception('AccessLevel dataset is invalid')

    result = []

    for al_row in dataset.Tables[0].Rows:
        access_level = AccessLevel(
            id=al_row.get_Item("AccessLevelID"),
            name=al_row.get_Item("AccessLevelName"))
        result.append(access_level)

    return result


def access_level_detail_to_py(access_level, dataset):
    """Convert Net2 access_level detail dataset
    time_zones is a net2-id key based lookup dict.
    """
    if not dataset or dataset.Tables.Count != 1:
        raise Exception('AccessLevelDetail dataset is invalid')

    # Clear existing
    access_level.details = []
    # Add details
    for ald_row in dataset.Tables[0].Rows:
        time_zone_id = ald_row.get_Item("TimezoneID")
        area_id = ald_row.get_Item("AreaID")
        access_level.details.append((time_zone_id, area_id))


def user_view_to_py(user_view):
    """Convert a Net2 UserView object (partially) to a dict
    """
    res = {}
    res["user_id"] = user_view.UserId
    res["access_level_id"] = user_view.AccessLevelId
    res["department_id"] = user_view.DepartmentId
    res["anti_passback_user"] = user_view.AntiPassbackUser
    res["alarm_user"] = user_view.AlarmUser
    res["first_name"] = user_view.FirstName
    res["middle_name"] = user_view.MiddleName
    res["sur_name"] = user_view.Surname
    res["telephone"] = user_view.Telephone
    res["extension"] = user_view.Extension
    res["pin"] = user_view.PIN
    res["activation_date"] = date_time_to_py(user_view.ActivationDate)
    res["active"] = user_view.Active
    res["fax"] = user_view.Fax
    res["expiry_date"] = date_time_to_py(user_view.ExpiryDate)
    res["custom_fields"] = [
        None,
        user_view.Field1_100,
        user_view.Field2_100,
        user_view.Field3_50,
        user_view.Field4_50,
        user_view.Field5_50,
        user_view.Field6_50,
        user_view.Field7_50,
        user_view.Field8_50,
        user_view.Field9_50,
        user_view.Field10_50,
        user_view.Field11_50,
        user_view.Field12_50,
        user_view.Field13_Memo,
        user_view.Field14_50]
    res["user_guid"] = user_view.UserGuid.ToString()
    res["last_area_id"] = user_view.LastAreaId
    res["last_access_time"] = date_time_to_py(user_view.LastAccessTime)
    res["last_updated"] = date_time_to_py(user_view.LastUpdated)

    return res
