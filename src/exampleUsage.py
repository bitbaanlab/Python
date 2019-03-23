import MALabLib
import sys
import os
import time


# clear the screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    print(" ____  _ _   ____                      __  __    _    _          _     ")
    print("| __ )(_) |_| __ )  __ _  __ _ _ __   |  \/  |  / \  | |    __ _| |__  ")
    print("|  _ \| | __|  _ \ / _` |/ _` | '_ \  | |\/| | / _ \ | |   / _` | '_ \ ")
    print("| |_) | | |_| |_) | (_| | (_| | | | | | |  | |/ ___ \| |__| (_| | |_) |")
    print("|____/|_|\__|____/ \__,_|\__,_|_| |_| |_|  |_/_/   \_\_____\__,_|_.__/ \n")

    serveraddress = input("Please insert API server address [Default=https://malab.bitbaan.com]: ")
    if serveraddress == "":
        serveraddress = "https://malab.bitbaan.com"

    malab = MALabLib.MALabLib(serveraddress)
    email = input("Please insert email address: ")
    password = input("Please insert your password: ")
    returnValue = malab.login(email, password)
    if returnValue["success"] is True:
        print("You are logged in successfully.")
    else:
        print("error code %d occured." % returnValue["error_code"])
        sys.exit(0)
    file_path = input("Please enter the path of file to scan: ")
    if os.path.isfile(file_path) is False:
        print("Cant read input file")
        sys.exit(0)
    file_name = os.path.basename(file_path)
    returnValue = malab.scan(file_path, file_name)
    if returnValue["success"] is True:
        # getting scan results:
        is_finished = False
        file_hash = malab.get_sha256(file_path)
        scan_id = returnValue["scan_id"]
        while is_finished is False:
            print("Waiting for getting results...")
            returnValue = malab.results(file_hash, scan_id)
            if returnValue["success"] is False:
                print("error code %d occurred." % returnValue["error_code"])
                sys.exit(0)
            cls()
            for current_av_result in returnValue["results"]:
                if current_av_result["result_state"] == 32:  # file is malware
                    print("%s ==> %s" % (current_av_result["av_name"], current_av_result["virus_name"]))
                elif current_av_result["result_state"] == 33:  # file is clean
                    print("%s ==> %s" % (current_av_result["av_name"], "Clean"))
            is_finished = returnValue["is_finished"]
            time.sleep(2)
    else:
        print("error code %d occurred." % returnValue["error_code"])
        sys.exit(0)
