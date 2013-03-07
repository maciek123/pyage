import os
import socket
from agent import Agent

workspace_name = "workspace@" + socket.gethostname() + ":" + str(os.getpid())

agents = [Agent()]
