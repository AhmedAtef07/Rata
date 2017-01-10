import os
import platform
import socket
import sys
import time

import psutil
import win32com.client
import wmi


def get_specs():
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(socket.gethostname())
    domainName = socket.getfqdn()
    systemPlatform = sys.platform
    machine = platform.machine()
    node = platform.node()
    processor = platform.processor()
    systemOS = platform.system()
    release = platform.release()
    version = platform.version()
    CPUsNum = psutil.cpu_count()
    pysicalCPUs = psutil.cpu_count(logical=False)
    sysBootTime = psutil.boot_time()
    timeZone = time.tzname[0]
    memory = psutil.virtual_memory()
    users = psutil.users()
    windowsDir = os.environ['windir']
    partitions = psutil.disk_partitions()
    # activeProcesses = psutil.pids()
    processes = wmi.WMI().Win32_Process()

    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(".", "root\cimv2")
    colItems = objSWbemServices.ExecQuery("Select * from Win32_BIOS")
    for objItem in colItems:
        BIOSVersion = objItem.BIOSVersion
        buildNumber = objItem.BuildNumber
        caption = objItem.Caption
        codeSet = objItem.CodeSet
        currentLanguage = objItem.CurrentLanguage
        description = objItem.Description
        identificationCode = objItem.IdentificationCode
        installableLanguages = objItem.InstallableLanguages
        installDate = objItem.InstallDate
        languageEdition = objItem.LanguageEdition
        languages = objItem.ListOfLanguages
        manufacturer = objItem.Manufacturer
        primaryBIOS = objItem.PrimaryBIOS
        releaseDate = objItem.ReleaseDate
        serialNumber = objItem.SerialNumber
        SMBIOSBIOSVersion = objItem.SMBIOSBIOSVersion
        SMBIOSMajorVersion = objItem.SMBIOSMajorVersion
        SMBIOSMinorVersion = objItem.SMBIOSMinorVersion
        SMBIOSPresent = objItem.SMBIOSPresent
        softwareElementID = objItem.SoftwareElementID
        softwareElementState = objItem.SoftwareElementState
        status = objItem.Status

    specs = ""
    specs += (
        "Hostname: " + hostname + "\n" +
        "IP Address: " + ipAddress + "\n" +
        "Full Qualified Domain Name: " + domainName + "\n" +
        "System Platform: " + systemPlatform + "\n" +
        "Machine: " + machine + "\n" +
        "Node: " + node + "\n" +
        "Pocessor: " + processor + "\n" +
        "System OS: " + systemOS + "\n" +
        "Release: " + release + "\n" +
        "Version: " + version + "\n" +
        "Number of CPUs: " + str(CPUsNum) + "\n" +
        "Number of Physical CPUs: " + str(pysicalCPUs) + "\n" +
        "System Boot Time: " + str(sysBootTime) + "\n" +
        "Time Zone: " + timeZone + "\n" +
        "Total Virtual Memory: " + str(memory[0]) + "\n" +
        "Available Memory: " + str(memory[1]) + "\n" +
        "Used Memory: " + str(memory[3]) + "\n" +
        "Free Memory: " + str(memory[4]) + "\n" +
        "Usage Percentage: " + str(memory[2]) + "\n" +
        "BIOS Version: " + str(BIOSVersion) + "\n" +
        "Build Number: " + str(buildNumber) + "\n" +
        "Caption: " + str(caption) + "\n" +
        "Code Set: " + str(codeSet) + "\n" +
        "Current Language: " + str(currentLanguage) + "\n" +
        "Description: " + str(description) + "\n" +
        "Identification Code: " + str(identificationCode) + "\n" +
        "Installable Languages: " + str(installableLanguages) + "\n" +
        "Install Date: " + str(installDate) + "\n" +
        "Language Edition: " + str(languageEdition) + "\n" +
        "List Of Languages: " + str(languages) + "\n" +
        "Manufacturer: " + str(manufacturer) + "\n" +
        "Primary BIOS: " + str(primaryBIOS) + "\n" +
        "Release Date: " + str(releaseDate) + "\n" +
        "Serial Number: " + str(serialNumber) + "\n" +
        "SMBIOS BIOS Version: " + str(SMBIOSBIOSVersion) + "\n" +
        "SMBIOS Major Version: " + str(SMBIOSMajorVersion) + "\n" +
        "SMBIOS Minor Version: " + str(SMBIOSMinorVersion) + "\n" +
        "SMBIOS Present: " + str(SMBIOSPresent) + "\n" +
        "Software Element ID: " + str(softwareElementID) + "\n" +
        "Software Element State: " + str(softwareElementState) + "\n" +
        "Status: " + status + "\n" +
        "Users: " + str(users) + "\n" +
        "Windows Directory: " + windowsDir + "\n" +
        "Disk Partitions: " + str(partitions) + "\n" +
        "\nActive Processes:\n"
    )

    # for process in processes:
    #     specs += ("\t" + str(process.ProcessId) + " - " + str(process.Name) + "\n")

    # for user in users:
    #     path = "C:/Users/" + user[0]
    #     dirs = os.listdir(path)
    #     specs += ("\n" + user[0] + " Directories:\n")
    #     for dirc in dirs:
    #         specs += ("\t" + dirc + "\n")
    #
    # for partition in partitions:
    #     path = partition[0]
    #     try:
    #         dirs = os.listdir(path)
    #         specs += ("\n" + partition[0] + " Directories:\n")
    #         for dirc in dirs:
    #             specs += ("\t" + dirc + "\n")
    #     except:
    #         specs += (path + " can't access\n")

    return serialNumber, specs


def main():
    x = get_specs()
    print len(x), x


if __name__ == "__main__":
    main()
