"""
Sample script to detect all SQLServer instances
"""

from Net2Scripting.network.sqlserver import SqlServerFinder


if __name__ == "__main__":

    inst = SqlServerFinder()
    print("Please wait for the servers to respond...")
    srvs = inst.find()
    if srvs:
        for s in srvs:
            print(s)
    else:
        print("No servers detected")
