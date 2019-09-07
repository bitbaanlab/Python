import MALabLib
import time
import sys
import os


# clear the screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


print(" ____  _ _   ____                      __  __    _    _          _     ")
print("| __ )(_) |_| __ )  __ _  __ _ _ __   |  \/  |  / \  | |    __ _| |__  ")
print("|  _ \| | __|  _ \ / _` |/ _` | '_ \  | |\/| | / _ \ | |   / _` | '_ \ ")
print("| |_) | | |_| |_) | (_| | (_| | | | | | |  | |/ ___ \| |__| (_| | |_) |")
print("|____/|_|\__|____/ \__,_|\__,_|_| |_| |_|  |_/_/   \_\_____\__,_|_.__/ \n")

serveraddress = input("Please insert API server address [Default=http://malabbeta.bitbaan.com]: ")
if serveraddress == "":
    serveraddress = "http://apimalabbeta.bitbaan.com"
malab = MALabLib.MALabLib(serveraddress)
email = input("Please insert email address: ")
password = input("Please insert your password: ")

return_value = malab.call_with_json_input('user/login', {'email': email, 'password': password})
if return_value["success"] is True:
    print("You are logged in successfully.")
else:
    malab.print_error(return_value)
    sys.exit(0)

apikey = return_value["apikey"]
file_path = input("Please enter the path of file to scan: ")
if os.path.isfile(file_path) is False:
    print("Can't read input file")
    sys.exit(0)
file_name = os.path.basename(file_path)
file_hash = malab.get_sha256(file_path)
return_value = malab.call_with_form_input('file/scan', {'file_path': file_path,
                                                        'file_name': file_name,
                                                        'apikey': apikey},
                                          'file_data', file_path)
if return_value["success"] is True:
    # getting scan results:
    is_finished = False
    while is_finished is False:
        print("Waiting for getting results...")
        return_value = malab.call_with_json_input('file/scan/result/get', {'hash': file_hash, 'apikey': apikey})
        if return_value["success"] is False:
            malab.print_error(return_value)
            sys.exit(0)
        cls()
        for current_av_result in return_value["scan"]["results"]:
            if current_av_result["result"] == "malware":  # file is malware
                print("%s ==> %s" % (current_av_result["av_name"], current_av_result["malware_name"]))
            elif current_av_result["result"] == "clean":  # file is clean
                print("%s ==> %s" % (current_av_result["av_name"], "Clean"))
        is_finished = return_value["scan"]["is_finished"]
        time.sleep(3)
else:
    malab.print_error(return_value)
    sys.exit(0)
