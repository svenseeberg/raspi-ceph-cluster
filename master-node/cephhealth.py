import time
import subprocess
import select


subprocess.Popen(['echo 470 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio470/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # green
subprocess.Popen(['echo 478 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio478/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # yellow
subprocess.Popen(['echo 479 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio479/direction'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # red



def led_on(pin):
	print(str(pin)+' On')
	subprocess.Popen(['echo 1 > /sys/class/gpio/gpio'+str(pin)+'/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def led_off():
	print('All Off')
	subprocess.Popen(['echo 0 > /sys/class/gpio/gpio470/value && echo 0 > /sys/class/gpio/gpio478/value && echo 0 > /sys/class/gpio/gpio479/value'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

while True:
	print("start iostat")
	f = subprocess.Popen(['sh -c "cd /home/cephadm/ceph && ceph --connect-timeout 10 health"'],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	p = select.poll()
	p.register(f.stdout)
	f.wait()
	
	line = f.stdout.readline().decode('UTF-8').split(' ')
	line = list(filter(None, line))
	print(line)
	if len(line) > 0 and line[0] == 'HEALTH_ERR':
		led_off()
		led_on(479)
	elif len(line) > 0 and line[0] == 'HEALTH_WARN':
		led_off()
		led_on(478)
	elif len(line) > 0 and line[0] == 'HEALTH_OK\n':
		led_off()
		led_on(470)
	else:
		led_off()
		led_on(478)
		led_on(479)
	time.sleep(1)
