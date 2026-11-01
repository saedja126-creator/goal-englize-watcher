import json,base64,glob,os,sys
out=sys.argv[1]
for f in sorted(glob.glob('/root/.claude/projects/-home-user-goal-englize-watcher/3795416f-4611-5512-bdea-dc096a1a5987/tool-results/mcp-Google_Drive-download_file_content-17930388*.txt')):
    d=json.load(open(f))
    t=d['title'].replace(' ','')
    open(os.path.join(out,t),'wb').write(base64.b64decode(d['content']))
    print(t,d['mimeType'])
