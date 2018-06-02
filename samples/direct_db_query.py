"""
Sample script to query the database directly
"""

from Net2Scripting.net2dbxs import Net2DBXS


if __name__ == "__main__":

    with Net2DBXS() as net2db:
        # Connect
        net2db.connect()
        # Get last log entry relating a device
        dataset = net2db.query_db(
            "select * from EventsEx "
            "where EventID = "
            "(select max(EventID) from sdk.EventsEx "
            " where SerialNumber is not NULL)")

        # Non result
        if (not dataset
                or dataset.Tables.Count < 1
                or dataset.Tables[0].Rows.Count < 1):

            print("Nothing relevant found")
        else:
            # Just to demonstrate how to get values from a dataset

            # Typically Table[0]
            table = dataset.Tables[0]
            # In this case only interested in the first row
            row = dataset.Tables[0].Rows[0]
            # For each column
            for col in table.Columns:
                val = row.get_Item(col.ColumnName)
                print("%s = %s" % (col.ColumnName, val))
