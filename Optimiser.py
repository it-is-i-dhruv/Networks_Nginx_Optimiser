# import
import os
import subprocess

# change directory to Nginx
os.chdir('/etc/nginx')

# optimisations
keepalive_timeout = "keepalive_timeout"
keepalive_requests = "keepalive_requests"

# optimisation of keepalive_timeout
def optimise_keepalive_timeout(line, conf):
    line = 'keepalive_timeout 60;\n'
    conf.append(line)

# optimisation of keepalive_requests
def optimise_keepalive_requests(line, conf):
    line = 'keepalive_requests 100;\n'
    conf.append(line)

optimised_conf = []
# open Nginx confuration file
with open('nginx.conf', 'r+') as conf:
    lines = conf.readlines()
    for line in lines:
        try:
            # check if line contains keepalive_timeout or keepalive_requests
            if keepalive_timeout in line:
                optimise_keepalive_timeout(line, optimised_conf)
                continue
            elif keepalive_requests in line:
                optimise_keepalive_requests(line, optimised_conf)
            optimised_conf.append(line)
        except:
            optimised_conf.append(line)
            continue
    
    # move file pointer to beginning and truncate file
    conf.seek(0)
    conf.truncate(0)
    
    # write optimised_conf back to conf
    for line in optimised_conf:
        conf.write(line)

# test
result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str = result.stdout.decode('utf-8')
stderr_str = result.stderr.decode('utf-8')

assert "is successful" in stderr_str