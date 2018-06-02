"""
Module offering base class for net2 access
"""


class Net2Base(object):
    """Net2 access base class
    """

    @classmethod
    def safe_get_row_val(cls, row, col):
        """Null aware fetching of row data

        Returns None if the database column is NULL
        """
    
        if row.IsNull(col):
            return None
        return row[col]
    

    @classmethod
    def dataset_to_str(cls, dataset):
        """Convert dataset to string presentation
        """

        if not dataset:
            return "None"
        if dataset.Tables.Count < 1:
            return "Empty"

        res = []
        for table in dataset.Tables:
            res.append("Table: %s" % (table.TableName))
            cols = []
            for col in table.Columns:
                cols.append(col.ColumnName)
            for row in table.Rows:
                row_res = []
                for i in range(len(cols)):
                    row_res.append("%s=%s" % (cols[i], row.get_Item(i)))
                res.append(", ".join(row_res))
        return "\n".join(res)
