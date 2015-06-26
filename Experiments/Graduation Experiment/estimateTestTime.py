import math

TEMP_TEST = 50
NRUNS = 3
NSCHEDULES = 3
NSERVERS = [4]
NCLIENTS = [1]

NQUESTS = 8
TEMP_TEST_LOC = 180

def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n /= 10
    return s

combinacoes = []
for comb in range(int(math.pow(10, NSCHEDULES+1))):
    for numClie in NCLIENTS:
        if comb % 10 == numClie:
            for numServ in NSERVERS:
                if sum_digits(int(comb/10)) == numServ:
                    combinacoes.append(comb)
print str(len(combinacoes))+" COMBINACOES DE TESTE:"
print combinacoes
tempo_teste = (TEMP_TEST * len(combinacoes))/60
print "TEMPO DE TESTE (HORAS)"
print "\tPOR RUN: "+str(tempo_teste/60)
print "\tTOTAL: "+str(tempo_teste*NRUNS/60)
print "NUM MAQUINAS PARA TEMPO TOTAL DE TESTE = 1 RUN: "+str(max(NSERVERS)*NRUNS+max(NCLIENTS)+1)
print "NUM MAQUINAS PARA TEMPO TOTAL DE TESTE = 1 RUN, COM SUPERCLIENT: "+str(max(NSERVERS)*NRUNS+1)
print "TOTAL DE QUESTS COMPUTADAS: "+str(len(combinacoes)*NQUESTS*NRUNS)
print "\tTEMPO PARA COMPUTA-LAS EM UMA MAQUINA (DIAS): "+str(len(combinacoes)*NQUESTS*NRUNS*TEMP_TEST_LOC/60/60/24)
