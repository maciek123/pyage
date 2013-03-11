import os
import socket
from pyage.core.agent import Agent

workspace_name = "workspace." + socket.gethostname() + "." + str(os.getpid())

agents = [Agent("makz")]
