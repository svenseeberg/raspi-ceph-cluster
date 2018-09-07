import time
import subprocess
import select

subprocess.Popen(['echo 474 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio474/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).wait()
f = subprocess.Popen(['iostat','-x','1'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

def led_on():
	print('On')
	subprocess.Popen(['echo 1 > /sys/class/gpio/gpio474/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def led_off():
	print('Off')
	subprocess.Popen(['echo 0 > /sys/class/gpio/gpio474/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

while True:
	line = f.stdout.readline().decode('UTF-8').split(' ')
	line = list(filter(None, line))
	if len(line) > 0 and (line[0] == 'sda' or line[0] == 'sdb'):
		if float(line[3].replace(',','.')) > 0:
			led_on()
			timeout = time.time() + 1
		if timeout > 0 and timeout < time.time():
			timeout = 0
			led_off()
