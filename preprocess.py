__author__ = "Baruch Baksht 211302088, Yisrael Rolnick 206672057"

import statistics


def convert2arff(ward):
    fout = open("ward" + str(ward) + ".arff", "w")
    fout.write("@relation patients_temperatures\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time_in_hours numeric\n")
    fout.write("@attribute temperature_in_C° numeric\n\n")
    fout.write("@data\n")

    fin = open(str(ward) + ".txt", "r")

    # Two-dimensional array in size: [number of patients in the ward][60 * 24].
    # Array rows for patients, array columns for minutes.
    temperatures = [[0] * (60 * 24) for i in range(numOfPatient(ward))]

    # Reading and filtering data from the ward file into the temperatures array
    for time in range(60 * 24):
        s = fin.readline().split()  # read row from ward file
        for patient in range(len(s)):
            temp = float(s[patient])
            if isInRange(temp):
                if float(temp) > 43.0:  # if temp in fahrenheits.
                    temperatures[patient][time] = fahrenheitToCelsius(temp)
                else:
                    temperatures[patient][time] = temp
            else:
                temperatures[patient][time] = None
    patient_Id = 0
    for patient in temperatures:  # (Each row in the "temperatures" array represents a patient)
        for hour in range(24):
            fout.write(str(patient_Id + 1) + "," + str(hour + 1) + "," + str(avgHour(patient, hour)) + "\n")
        patient_Id += 1
    fin.close()
    fout.close()


def fahrenheitToCelsius(fahrenheit):
    """
    Function to convert Celsius to Fahrenheit
    :param Fahrenheit: Fahrenheit
    :type Fahrenheit: float
    :return: Celsius
    :rtype:float
    """
    return (fahrenheit - 32) * (5.0 / 9)


def isInRange(temperature):
    """
    Checks whether a particular temperature is within the correct temperature range
    :param temperature: temperature
    :type temperature: float
    :return: True if temperature in range
    :rtype: int
    """
    if 36.0 <= temperature <= 43.0 or 36.0 <= fahrenheitToCelsius(temperature) <= 43.0:
        return True
    else:
        return False


def numOfPatient(ward):
    """
    Returns the number of patients in a particular ward
    :param ward: The particular ward
    :type ward: int
    :return: The number of patients
    :rtype: int
    """
    fin = open(str(ward) + ".txt", "r")
    ret = len(fin.readline().split())
    fin.close()
    return ret


def avgHour(patient, hour):
    """
    To calculate the average hourly temperature for a patient
    :param patient: One-dimensional array with all temperature measurements (per minute) for a particular patient
    :type patient: list
    :param hour: The hour for which the average is calculated
    :type hour: int
    :return: average hourly temperature for a patient
    :rtype: float
    """
    indexes = [0] * 60
    for i in range(60):
        indexes[i] = (hour * 60) + i
    ret = [patient[x] for x in indexes]
    _sum = 0
    count = 0
    for i in ret:
        if i is not None:
            _sum += i
            count += 1
    return round(_sum / count, 1)


def _variance(fileName):
    """
    To calculate variance of the temperatures of a particular class
    :param fileName: The file name of the ward
    :type fileName: string
    :return: The variance
    :rtype: float
    """
    with open(fileName) as f:
        lines = f.read()
    tempList = lines.split()[12:]  # type: list
    _list = []
    for i in range(len(tempList)):
        _list.append(float(tempList[i].split(',')[2]))
    return statistics.variance(_list)


convert2arff(1)
convert2arff(2)
convert2arff(3)

print("Temperature variance for ward 1:", round(_variance("ward1.arff"), 5))
print("Temperature variance for ward 1:", round(_variance("ward2.arff"), 5))
print("Temperature variance for ward 1:", round(_variance("ward3.arff"), 5))
