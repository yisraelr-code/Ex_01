def convert2arff(ward):
    fout = open("ward" + str(ward) + ".arff", "w")
    fout.write("@relation patients_temperatures\n")
    #fout.write("@attribute ward numeric\n")
    fout.write("@attribute patients_ID numeric\n")
    fout.write("@attribute time_in_hours numeric\n")
    fout.write("@attribute temperature_in_C° numeric\n\n")
    fout.write("@data\n")

    fin = open(str(ward) + ".txt", "r")
    temperatures = [[0] * (60 * 24) for i in range(numOfPatient(ward))]
    for time in range(60 * 24):
        s = fin.readline().split()
        for patient in range(len(s)):
            temp = float(s[patient])
            if isInRange(temp):
                if float(temp) > 43.0:
                    temperatures[patient][time] = fahrenheitToCelsius(temp)
                else:
                    temperatures[patient][time] = temp
            else:
                temperatures[patient][time] = None
    patient_Id = 0
    for patient in temperatures: # line after line
        for hour in range(24):
            fout.write(str(patient_Id + 1) + "," + str(hour + 1) + "," + str(avgHour(patient, hour)) + "\n")
        patient_Id += 1
    fin.close()
    fout.close()


def fahrenheitToCelsius(fahrenheit):
    return (fahrenheit - 32) * (5.0 / 9)


def isInRange(temperature):
    if 36.0 <= temperature <= 43.0 or 36.0 <= fahrenheitToCelsius(temperature) <= 43.0:
        return True
    else:
        return False


def numOfPatient(ward):
    fin = open(str(ward) + ".txt", "r")
    ret = len(fin.readline().split())
    fin.close()
    return ret


def avgHour(patient, hour):
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
    return _sum / count


convert2arff(1)
convert2arff(2)
convert2arff(3)
