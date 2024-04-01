import os
import subprocess
import re

# path = os.chdir('/etc/nginx')

opt_params = {"worker_processes" }

def worker_process_opt(work, conf):
    print("worker process found, triggering function worker_process_opt")
    # print(work)
    # print(work.strip().split()[1])
    work_split = work.strip().split()
    
    #cat /proc/cpuinfo | grep "cpu cores" | head -1 just spread over
    cpuinfo = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    grep_cores = subprocess.run(['grep', 'cpu cores'], input=cpuinfo.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    head = subprocess.run(['head', '-1'], input=grep_cores.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cores_line= head.stdout.decode('utf-8')
    cores = cores_line.strip().split()[3]
    # print(cores)
    # print(type(cores))
    work_split[1] = '{};\n'.format(cores)
    # print(work_split)
    final_line = ' '.join(work_split)
    print('optimisation done: ',final_line)
    conf.append(final_line)
    return None

# Cache the static content in the server
def cache_opt(output_path=None):
    print("cache not found, triggering function cache_opt")
    # Define caching settings to be added
    caching_settings = """
    # Static file caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    """

    # Ensure output_path is set
    if output_path is None:
        output_path = "nginx.conf"

    # Read the original nginx.conf
    with open("nginx.conf", 'r') as file:
        config_contents = file.read()

    # Find the http block and insert caching settings
    http_block_pattern = r'(http\s*\{)'
    modified_contents = re.sub(http_block_pattern, r'\1' + caching_settings, config_contents, count=1)
    # Write the modified configuration back to the file
    with open(output_path, 'w') as file:
        file.write(modified_contents)

    print(f'Updated Nginx configuration has been saved to {output_path}')


    


comments = []
with open('nginx.conf', 'r+') as config:
    lines = config.readlines()
    cache_opt()
    print(lines)
    for i in lines:
        try:
            # print(i[-2])+
            # print(i.strip().split())
            if i.strip().split()[0] in opt_params :
                print("i:", i)
                print("comments: ", comments)
                worker_process_opt(i, comments)
                continue
            # if "worker_processes" in i:
            #     worker_process_opt(i) 
            # if i[-2] == ';':
            #     # print(i)
            #     continue
            comments.append(i)
        except:
            comments.append(i)
            continue
    # print(comments)
    # assert comments == lines
    config.seek(0)
    config.truncate(0)
    for line in comments:
        config.write(line)
    
cache_opt()

#at the end just replace conf with comments
#check for nginx -t
# result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE)
# checker = str(result.stdout.decode('utf-8'))
# print(checker)
# assert "is successful" in checker
# result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# stdout_str = result.stdout.decode('utf-8')
# stderr_str = result.stderr.decode('utf-8')

# print(stdout_str)
# print(stderr_str)
#no idea why it outputs to stderr instead of stdout......
# assert "is successful" in stderr_str