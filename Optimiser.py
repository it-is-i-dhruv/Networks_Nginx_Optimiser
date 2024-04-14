import os
import subprocess

# Change directory to Nginx configuration directory
os.chdir('/etc/nginx')

# Define the optimization parameter
opt_param = "tcp_nopush"

# Function to optimize the tcp_nopush directive
def optimize_tcp_nopush(line, conf):
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
# Open the Nginx configuration file
with open('nginx.conf', 'r+') as config:
    lines = config.readlines()
    for line in lines:
        try:
            # Check if the current line contains the optimization parameter
            if opt_param in line:
                optimize_tcp_nopush(line, comments)
                continue
            comments.append(line)
        except:
            comments.append(line)
            continue
    
    # Move the file pointer to the beginning and truncate the file
    config.seek(0)
    config.truncate(0)
    
    # Write the optimized configuration back to the file
    for line in comments:
        config.write(line)

# Test the Nginx configuration after optimization
result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str = result.stdout.decode('utf-8')
stderr_str = result.stderr.decode('utf-8')

# Print the result of the configuration test
print(stderr_str)
assert "is successful" in stderr_str
