# pylint: disable=missing-module-docstring,missing-function-docstring,invalid-name,consider-iterating-dictionary
import datetime

def TransformData(dataInit):

    data = []

    output = dataInit[0]

    for line in output.splitlines():
        line = line.split()
        if line[0] == "Mem:":
            memPercent = (int(line[2])/int(line[1])) * 100
            data.append(memPercent)

    output = dataInit[1]
    lines = output.splitlines()[0]
    line = lines.split(" ")
    cpu = (int(line[2])+int(line[4])*100)/(int(line[2])+int(line[4])+int(line[5]))

    data.append(cpu)

    data.append(int(dataInit[2]))

    return data

def GetLog(output):

    lines = output.split("\n")
    logs=[]

    for line in lines:
        
        line = line.split(" ")
        if line[0] != "":
            source = line[0]
            date = line[3][1:]
            page = line[6]
            answer = line[8]
            log = [source,date,page,answer]
            logs.append(log)

    return logs


def GetStatByPage(logs):

    statByPage = {}

    for line in logs:
        if line[2][0] == "/":
            if line[2] in statByPage.keys():
                statByPage[line[2]] += 1
            else:
                statByPage[line[2]] = 1

    return statByPage

def FusionDico(dico1,dico2):
    dicoA = dico1.copy()
    dicoB = dico2.copy()
    dicoC = dicoA.copy()

    for keyB in dicoB.keys():
        if keyB in dicoC.keys():
            dicoC[keyB] += dicoB[keyB]
        else:
            dicoC[keyB] = dicoB[keyB]

    return dicoC

def GetActivityLastMinute(output):

    length = int(output.split(" ")[0])

    return length

def GetLogsByTime(logs, nb_hour_diff):
    tmp_logs = []
    now = datetime.datetime.now()
    for line in logs:
        t = line[1]
        t_to_time = datetime.datetime.strptime(t, '%d/%b/%Y:%H:%M:%S')
        t_to_time = t_to_time + datetime.timedelta(hours = nb_hour_diff)

        if(t_to_time>=now) : tmp_logs.append(line)
    return tmp_logs
    
def GetStatByConnection(logs):

    statByConnection = {}
    for line in logs:
        if line[0] in statByConnection.keys():
            statByConnection[line[0]] += 1
        else:
            statByConnection[line[0]] = 1

    return statByConnection

def GetNb404(logs):

    count = 0

    for line in logs:
        if line[3] == "404":
            count += 1

    return count

def GetStatBy404(logs):

    statBy404 = {}

    for line in logs:
        if line[3] == "404":
            if line[2] in statBy404.keys():
                statBy404[line[2]] += 1
            else:
                statBy404[line[2]] = 1

    return statBy404
