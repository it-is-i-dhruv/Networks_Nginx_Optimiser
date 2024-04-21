import os
import subprocess
import re

# path = os.chdir('/etc/nginx')

opt_params = {"worker_processes", "tcp_nopush" }

def worker_processes_opt(work, conf):
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

def modify_nginx_config(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Regular expressions to detect configurations
    re_http_block = re.compile(r'^\s*http\s*{')
    re_server_block = re.compile(r'^\s*server\s*{')
    re_proxy_cache_path = re.compile(r'^\s*proxy_cache_path')
    re_proxy_cache = re.compile(r'^\s*proxy_cache')
    re_proxy_pass = re.compile(r'^\s*proxy_pass')
    re_proxy_cache_valid = re.compile(r'^\s*proxy_cache_valid')

    cache_path_found = False
    http_block_index = None

    # Search for HTTP block and proxy_cache_path
    for i, line in enumerate(lines):
        if re_http_block.match(line):
            http_block_index = i
        if http_block_index is not None and re_proxy_cache_path.match(line):
            cache_path_found = True
            break

    # Prompt for cache location if not found
    if not cache_path_found:
        cache_location = input("Enter the location for cache (leave blank for '/var/cache/nginx'): ") or "/var/cache/nginx"
        cache_config = f"    proxy_cache_path {cache_location} keys_zone=mycache:10m;\n"
        lines.insert(http_block_index + 1, cache_config)

    # Process each server block
    in_server_block = False
    for i in range(len(lines)):
        if re_server_block.match(lines[i]):
            in_server_block = True
            server_start_index = i
            proxy_cache_inserted = False
        
        if in_server_block and re_server_block.match(lines[i]):
            # Insert proxy_cache mycache if not present in server block
            if not proxy_cache_inserted:
                lines.insert(server_start_index + 1, "        proxy_cache mycache;\n")
                proxy_cache_inserted = True

        if in_server_block and re_http_block.match(lines[i]):
            in_server_block = False
        
        # Check for proxy_pass and add proxy_cache_valid if not present
        if in_server_block and re_proxy_pass.match(lines[i]):
            if i+1 < len(lines) and not re_proxy_cache_valid.match(lines[i+1]):
                lines.insert(i + 1, "            proxy_cache_valid 200 302 60m;\n")

    # Write the modified configuration back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

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
    print(lines)
    for i in lines:
        try:
            # print(i[-2])+
            # print(i.strip().split())
            # print(i.strip().split()[0][1:])
            if i.strip().split()[0] in opt_params   :
                print("i:", i)
                print("comments: ", comments)
                print(globals())
                # worker_process_opt(i, comments)
                print(i.strip().split()[0]+ "_opt")
                globals()[i.strip().split()[0]+ "_opt"](i, comments)
                continue
            elif i.strip().split()[0][1:] in opt_params: 
                print("i:", i)
                print("comments: ", comments)
                print(globals())
                # worker_process_opt(i, comments)
                print(i.strip().split()[0]+ "_opt")
                globals()[i.strip().split()[0][1:]+ "_opt"](i, comments)
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

# modify_nginx_config('nginx.conf')
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