import os
import subprocess

path = os.chdir('/etc/nginx')

opt_params = {"worker_processes"}

def worker_process_opt(work):
    print("worker process found")
    print(work)
    print(work.strip().split()[1])
    work_split = work.strip().split()
    work_split[1] = '3;'
    print(work_split)
    print(' '.join(work_split))
    return None


comments = []
with open('nginx.conf', 'r+') as config:
    lines = config.readlines()
    print(lines)
    for i in lines:
        try:
            # print(i[-2])+
            # print(i.strip().split())
            if i.strip().split()[0] in opt_params :
                print(i)
                print(worker_process_opt(i) )
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

#at the end just replace conf with comments
#check for nginx -t
# result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE)
# checker = str(result.stdout.decode('utf-8'))
# print(checker)
# assert "is successful" in checker
result = subprocess.run(['nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout_str = result.stdout.decode('utf-8')
stderr_str = result.stderr.decode('utf-8')

# print(stdout_str)
print(stderr_str)
#no idea why it outputs to stderr instead of stdout......
assert "is successful" in stderr_str