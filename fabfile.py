from fabric.api import *
import os

hosts = ['localhost:' + str(port) for port in range(9000, 9005)]
ns = '172.16.129.54'

def host_type():
	env.hosts = ['localhost:' + str(port) for port in range(9000, 9005)]
	run('uname -s')

def update():
	execute(run_update, hosts = hosts)

def run_update():
    sudo('apt-get -y --no-upgrade install python-setuptools')
    sudo('sudo easy_install -U pyage Pyro4==4.17')

def matplotlib():
	execute(run_matplotlib, hosts = hosts)

def run_matplotlib():
	sudo('apt-get update')
	sudo('apt-get install libfreetype6-dev libpng-dev python-numpy gcc g++ python2.7-dev -y')
	sudo('sudo easy_install matplotlib')

def send_conf():
    execute(send, hosts = hosts)

def send():
    put('pyage_conf', '~/')


@parallel
def evolution():
	agents_count = 180
	for i in range(6,0,-1):
		h = hosts[:i]
		execute(run_evolution, agents_count/i, ns, hosts=h)

@parallel
def run_evolution(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.fconf")

@parallel
def aggregate():
	agents_count = 180
	for i in range(6,0,-1):
		h = hosts[:i]
		execute(run_aggregate, agents_count/i, ns, hosts=h)

@parallel
def run_aggregate(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.fagg_conf")

@parallel
def emas():
	agents_count = 60
	for i in range(len(hosts),0,-1):
		h = hosts[:i]
		execute(run_emas, agents_count/i, ns, hosts=h)

@parallel
def run_emas(agents_count, ns_hostname):
	with shell_env(AGENTS=str(agents_count),NS_HOSTNAME=ns_hostname):
		run("export PYRO_HOST=$(ip addr show eth0 | grep -o 'inet [0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+' | grep -o [0-9].*); python -m pyage.core.bootstrap pyage.conf.femas_conf")

