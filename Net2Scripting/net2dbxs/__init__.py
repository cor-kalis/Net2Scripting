"""
The module that offers direct access to the Paxton Net2 database,
not using the SDK.
"""
import clr

from threading import RLock

clr.AddReference('System.Data')
from System.Data.SqlClient import SqlConnection, SqlDataAdapter, SqlCommand
from System.Data import DataSet, CommandType, ParameterDirection

from Net2Scripting.net2base import Net2Base
from Net2Scripting.pylog4net import Log4Net


class Net2DBXSException(Exception):
    """Exception class for net2 database xs
    """
    pass


class DBCommand(object):
    """With wrapper for SqlCommand
    """
    def __init__(self, query, con):
        self._cmd = SqlCommand(query, con)

    def __enter__(self):
        return self._cmd

    def __exit__(self, type, value, traceback):
        if (self._cmd):
            self._cmd.Dispose()


class Net2DBXS(Net2Base):
    """Net2 direct database access class
    """

    # Class variables
    _logger = Log4Net.get_logger('Net2DBXS')
    _lock = RLock()

    def __init__(self):
        """Class constructor
        """
        self._con = None
        self._connected = False

    def __enter__(self):
        """With enter
        """
        return self

    def __exit__(self, type, value, traceback):
        """With exit
        """
        self.dispose()

    def _check_connect(self):
        """Check database connection
        Raises Net2DBXSException if not connected.
        """
        if not self._connected:
            raise Net2DBXSException("Not connected to the database")

    def connect(self,
                user_name="sdk_user",
                password="E56ABED4-2918-44F9-A110-71B61B47142A",
                db='Net2',
                server=None):
        """Connect to database

        If the server parameter is None, named pipes are used.
        For remote connections, the server parameter should contain the
        windows name.
        """
        self.dispose()

        with Net2DBXS._lock:
            if not server:
                Net2DBXS._logger.Debug('Connecting through named pipes')
                self._con = SqlConnection(
                    r"server=\\.\pipe\MSSQL$NET2\sql\query;database=%s;uid=%s;password=%s" %
                    (db, user_name, password))
            else:
                Net2DBXS._logger.Debug('Connecting over the network')
                self._con = SqlConnection(
                    r"server=%s\NET2;database=%s;uid=%s;password=%s" %
                    (server, db, user_name, password))
            self._con.Open()
            self._connected = True
            Net2DBXS._logger.Debug('Connected')

    def query_db(self, query):
        """Perform database query and return data in dataset

        Returns a dataset.
        """
        self._check_connect()

        with DBCommand(query, self._con) as cmd:
            adapter = SqlDataAdapter()
            adapter.SelectCommand = cmd
            data = DataSet()
            adapter.Fill(data)

        return data

    def run_stored_procedure(self, sp_name, **params):
        """Run stored procedured

        Returns the stored procedure result value.
        """
        with DBCommand(sp_name, self._con) as cmd:
            cmd.CommandType = CommandType.StoredProcedure
            # Add parameters
            for name, value in params.iteritems():
                cmd.Parameters.AddWithValue("@%s" % name, value)
            # Add return code
            cmd.Parameters.AddWithValue("@result", -1)
            cmd.Parameters["@result"].Direction = ParameterDirection.ReturnValue
            # Execute
            cmd.ExecuteNonQuery()
            return cmd.Parameters["@result"].Value

    def get_all_tables(self):
        """Convenience function to retrieve all known tables / views

        Returns a dataset.
        """
        return self.query_db(
            "select * from INFORMATION_SCHEMA.Tables order by TABLE_NAME")

    def dispose(self):
        """Dispose database connection
        """
        with Net2DBXS._lock:
            if self._con:
                try:
                    self._con.Close()
                    self._con = None
                    Net2DBXS._logger.Debug('Disposed')
                except:
                    pass
