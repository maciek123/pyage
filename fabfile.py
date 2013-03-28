from fabric.api import *


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

@parallel
def evolution():
	hosts = ['localhost:' + str(port) for port in range(9000, 9018)]
	ns = ['172.16.145.101', '172.16.145.104', '172.16.145.106', '172.16.145.160', '172.16.145.161']
	agents_count = 8
	for i in range(1,5):
		h = hosts[:2**i]
		execute(run_evolution, agents_count, ns[0], hosts=h)
		agents_count /= 2
		raw_input("press enter")

@parallel
def run_evolution(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.fconf")

@parallel
def aggregate():
	hosts = ['localhost:' + str(port) for port in range(9000, 9018)]
	ns = ['172.16.145.101', '172.16.145.104', '172.16.145.106', '172.16.145.160', '172.16.145.161']
	agents_count = 16
	for i in range(5):
		h = hosts[:2**i]
		execute(run_aggregate, agents_count, ns[0], hosts=h)
		agents_count /= 2
		raw_input("press enter")

@parallel
def run_aggregate(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.fagg_conf")

@parallel
def emas():
	hosts = ['localhost:' + str(port) for port in range(9000, 9018)]
	ns = ['172.16.145.101', '172.16.145.104', '172.16.145.106', '172.16.145.160', '172.16.145.161']
	agents_count = 16
	for i in range(5):
		h = hosts[:2**i]
		execute(run_emas, agents_count, ns[0], hosts=h)
		agents_count /= 2
		raw_input("press enter")

@parallel
def run_emas(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.femas_conf")


def get_logs():
	get("/home/makz/pyage*.log", "logs/"+env.host_string+"/")

def ns():
	execute(run_ns, hosts = ['localhost:9001'])

def run_ns():
	run("./run_ns.sh")

def killns():
	execute(kill_ns, hosts = ['localhost:9001'])

def kill_ns():
	run("kill `cat pid`")
