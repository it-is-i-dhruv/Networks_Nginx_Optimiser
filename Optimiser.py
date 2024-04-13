import os
import subprocess

path = os.chdir('/etc/nginx')

opt_params = {"tcp_nopush"}  # Add 'tcp_nopush' to the optimization parameters

def tcp_nopush_opt(line, conf):
    print("tcp_nopush directive found, triggering optimization")
    # Check if the directive is already set to 'on'
    if 'tcp_nopush on' not in line:
        # Replace any existing 'tcp_nopush' directive with 'tcp_nopush on'
        line = 'tcp_nopush on;\n'
        print('Optimization done: tcp_nopush on')
    else:
        print('tcp_nopush directive already optimized')
    conf.append(line)

comments = []
with open('nginx.conf', 'r+') as config:
    lines = config.readlines()
    for line in lines:
        try:
            # Check if the current line contains an optimization parameter
            if any(param in line for param in opt_params):
                tcp_nopush_opt(line, comments)
                continue
            comments.append(line)
        except:
            comments.append(line)
            continue
    
    config.seek(0)
    config.truncate(0)
    for line in comments:
        config.write(line)

# Test the Nginx configuration after optimization
result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str = result.stdout.decode('utf-8')
stderr_str = result.stderr.decode('utf-8')

print(stderr_str)
assert "is successful" in stderr_str
