import json,base64
T='/root/.claude/projects/-home-user-goal-englize-watcher/3795416f-4611-5512-bdea-dc096a1a5987/tool-results/mcp-Google_Drive-download_file_content-'
m={'1792590746142':1,'1792590746167':2,'1792590746611':3,'1792590746774':4,'1792590747320':5,'1792590747829':6,'1792590748130':7}
for k,n in m.items():
    d=json.load(open(T+k+'.txt'))
    b=base64.b64decode(d['content'])
    open(f'como_in/slide{n}.bin','wb').write(b)
    print(n,d['title'],len(b),b[:4])
