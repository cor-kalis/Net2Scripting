"""
Sample script to detect Net2Plus modules
"""

from Net2Scripting.network.net2plus import Net2PlusFinder


if __name__ == "__main__":

    inst = Net2PlusFinder()
    print("Please wait for the modules to respond...")
    devs = inst.find()
    if devs:
        for d in devs:
            print(d)
    else:
        print("No devices detected")
