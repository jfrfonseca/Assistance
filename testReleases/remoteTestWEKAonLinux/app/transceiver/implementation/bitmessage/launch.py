from subprocess import Popen, PIPE

process = Popen(['python', 'bitmessagemain.py'], stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()