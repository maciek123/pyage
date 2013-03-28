from fabric.api import *

ns_hostname = '172.16.145.101'

def host_type():
	env.hosts = ['localhost:' + str(port) for port in range(9000, 9018)]
	run('uname -s')

def update():
	execute(run_update, hosts = ['localhost:' + str(port) for port in range(9000, 9018)])

def run_update():
	sudo('sudo easy_install -U pyage')

def matplotlib():
	sudo('apt-get update')
	sudo('apt-get install libfreetype6-dev libpng-dev python-numpy gcc g++ python2.7-dev -y')
	sudo('sudo easy_install matplotlib')

def evolution():
	hosts = ['localhost:' + str(port) for port in range(9000, 9018)]
	agents_count = 16
	for i in range(5):
		h = hosts[:2**i]
		execute(run_evolution, agents_count,hosts=h)
		agents_count /= 2

def run_evolution(agents_count):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("echo $AGENTS")
		#run("python -m pyage.core.bootstrap pyage.conf.fconf")

def aggregate(agents_count):
	with shell_env(AGENTS=agents_count,NS_HOSTNAME=ns_hostname):
		run("python -m pyage.core.bootstrap pyage.conf.fagg_conf")

def get_logs():
	get("/home/makz/pyage*.log", "logs/"+env.host_string+"/")

def ns():
	execute(run_ns, hosts = ["localhost:9000"])

def run_ns():
	run("nohup python -Wignore -m Pyro4.naming -n 172.16.145.101 &", pty=False)
