# -*- coding: utf-8 -*-

import chilkat
import os,os.path
import Log

encryptPassword = "MIGfMA+dgdsagdsagdsagdasggggggggggg56CpgaRMm1/+Tzd2TQIDAQAB"

def zip_encrypt(file_path, zip_path):
    filelist = ""
    if os.path.isfile(file_path):
        filelist = file_path;
    else:
        filelist = file_path + "/*";

    zip = chilkat.CkZip()
    #  Any string unlocks the component for the 1st 30-days.
    success = zip.UnlockComponent("Anything for 30-day trial")
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False
        # sys.exit()

    success = zip.NewZip(zip_path)
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False
        # sys.exit()

    #  Set properties to indicate that the Zip should be
    #  AES encrypted.
    #  A value of 4 indicates WinZip compatible AES encryption.
    zip.put_Encryption(4)
    #  Key length can be 128, 192, or 256 bits.
    zip.put_EncryptKeyLength(128)
    #  Set the password for AES encryption:
    zip.put_EncryptPassword(encryptPassword)
    #  Add a directory tree to be zipped.  (The files
    #  are not compressed at this point -- only references
    #  to the files and directories are added to the zip object.)
    recurse = True
    success = zip.AppendFiles(filelist, recurse)
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False

        #  Create the encrypted zip ("/myZipDir/aes.zip")
        #  The path of the zip is what was originally passed
        #  to the NewZip method (above).

    success = zip.WriteZipAndClose()
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False

    print("Created AES Encrypted Zip success.")
    Log.logger.info(zip_path + "Created AES Encrypted Zip success.")

    return True


def zip_dencrypt(zip_file, unzip_dir):
    zip = chilkat.CkZip()

    #  Any string unlocks the component for the 1st 30-days.
    success = zip.UnlockComponent("Anything for 30-day trial")
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False

    success = zip.OpenZip(zip_file)
    if (success != True):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False

    # Set the password needed to unzip.
    #  This password must match the password used when the zip
    #  was created.
    zip.put_DecryptPassword(encryptPassword)

    #  Unzip the .zip into /unzipDir.
    #  Returns the number of files and directories unzipped.
    unzipCount = zip.Unzip(unzip_dir)
    if (unzipCount < 0):
        print(zip.lastErrorText())
        Log.logger.error(zip.lastErrorText())
        return False
    else:
        print("unzip dencrypted file success!")
        Log.logger.info(unzip_dir + ":unzip dencrypted file success!")

    return True

# if __name__ == '__main__':
    # filePath = "12345678.90"
    # filename = "90"
    # length = len(filePath) - len(filename) - 1
    # targetPath = filePath[0:length] + ".zip"
    # print(targetPath)

#     # zip_encrypt("D:\\test\\logs", "D:\\test\\logs.zip")
#     zip_encrypt( "D:\\test\\logs", "D:\\test\\logs.zip")
#     # zip_dencrypt(r'D:\\test\\zf_b2c\\logs.zip',r'D:\\test\\zf_b2c\\log')