# Replacing shell pipeline
# output=`dmesg | grep hda`
# becomes:
import subprocess
from subprocess import Popen, PIPE
p1 = Popen(["echo"], stdout=PIPE)
p2 = Popen(["ls", "-la"], stdin=p1.stdout, stdout=PIPE).communicate()[0]
print(p2)
# p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.

# output = p2.communicate()[0]
# print(output)
#Alternatively:
# output=`dmesg | grep hda`
# becomes:

