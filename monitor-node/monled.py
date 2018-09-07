import time
import subprocess
import select


subprocess.Popen(['echo 470 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio470/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # green
subprocess.Popen(['echo 478 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio478/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # yellow
subprocess.Popen(['echo 479 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio479/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # red



def led_on(pin):
	print(str(pin)+' On')
	subprocess.Popen(['echo 1 > /sys/class/gpio/gpio'+str(pin)+'/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def led_off(pin):
	print('All Off')
	subprocess.Popen(['echo 0 > /sys/class/gpio/gpio'+str(pin)+'/value '],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def led_blink(pin):
	subprocess.Popen(['echo 1 > /sys/class/gpio/gpio'+str(pin)+'/value && sleep 0.4 && echo 0 > /sys/class/gpio/gpio'+str(pin)+'/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

prev_epoch = 0
while True:
	f = subprocess.Popen(['sh -c "ceph status"'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p = select.poll()
	p.register(f.stdout)
	try:
		f.wait(timeout=10)
	except subprocess.TimeoutExpired:
		f.kill()
		led_blink(479)
		continue
	while True:
		line = f.stdout.readline().decode('UTF-8').split(' ')
		line = list(filter(None, line))
		if len(line) > 0 and line[0] == 'election' and line[1] == 'epoch' and int(line[2].replace(',','')) > prev_epoch:
			print(line[-1])
			led_blink(478)
			prev_epoch = int(line[2].replace(',',''))
		if len(line) > 0 and line[0] == 'election' and line[1] == 'epoch' and 'r3n1' in line[-1]:
			led_blink(470)
			break
		elif len(line) > 0 and line[0] == 'election' and line[1] == 'epoch':
			print(line[-1])
			led_blink(479)
			break
		if len(line) == 0:
			led_blink(479)
			break
