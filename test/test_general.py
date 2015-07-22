import threading
import time
import sys

from busybees import worker
from busybees import hive

import pash

class ErrWorker(worker.Worker):
	def work(self, command):
		proc = pash.ShellProc()
		proc.run(command)
		return "Exit code: %s" % proc.get_val('exit_code')

def test_hive():
	apiary = hive.Hive()
	apiary.create_queen('A1')

	apiary.create_queen('A2')

	apiary.start_queen('A1')

	apiary.start_queen('A2')

	jobs = ["iscsiadm -m discovery -t st -p 192.168.88.110",
            "iscsiadm -m discovery -t st -p 192.168.90.110",
            "iscsiadm -m discovery -t st -p 192.168.88.110"]
	apiary.instruct_queen('A1', jobs, ErrWorker)

	apiary.kill_queen('A1')

	time.sleep(3)

	this = apiary.die()

	for key in this.keys():
		for i in this[key]:
			print i

	sys.exit(0)
