import MALabLib
import sys
import os

if __name__ == "__main__":
    print(" ____  _ _   ____                      __  __    _    _          _     ")
    print("| __ )(_) |_| __ )  __ _  __ _ _ __   |  \/  |  / \  | |    __ _| |__  ")
    print("|  _ \| | __|  _ \ / _` |/ _` | '_ \  | |\/| | / _ \ | |   / _` | '_ \ ")
    print("| |_) | | |_| |_) | (_| | (_| | | | | | |  | |/ ___ \| |__| (_| | |_) |")
    print("|____/|_|\__|____/ \__,_|\__,_|_| |_| |_|  |_/_/   \_\_____\__,_|_.__/ \n")

    serveraddress = input("Please insert API server address [Default=https://malab.bitbaan.com]: ")
    if serveraddress == "":
        serveraddress = "http://multiavbeta.bitbaan.com"

    malab = MALabLib.MALabLib(serveraddress)
    email = input("Please insert email address: ")
    password = input("Please insert your password: ")
    returnValue = malab.login(email, password)
    if returnValue["success"] is True:
        print("You are logged in successfully.")
    else:
        print("error code %d occured." % returnValue)
        sys.exit(0)
    file_path = input("Please enter the path of file to scan: ")
    if os.path.isfile(file_path) is False:
        print("Cant read input file")
        sys.exit(0)
    file_name = os.path.basename(file_path)
    returnValue = malab.scan(file_path, file_name)
    if returnValue["success"] is True:
        print("Scan completed successfully.")
    else:
        print("error code %d occurred." % returnValue)
        sys.exit(0)
