import json,base64,sys
T='/root/.claude/projects/-home-user-goal-englize-watcher/3795416f-4611-5512-bdea-dc096a1a5987/tool-results/mcp-Google_Drive-download_file_content-'
m={'1792511225958':'slide2','1792511230929':'slide1','1792511231641':'slide3','1792511233400':'slide4','1792511232518':'slide5','1792511232940':'slide6','1792511233226':'slide7'}
for k,n in m.items():
    d=json.load(open(T+k+'.txt'))
    b=base64.b64decode(d['content'])
    open(f'drive_in/{n}.bin','wb').write(b)
    print(n,d['title'],d['mimeType'],len(b),b[:4])
