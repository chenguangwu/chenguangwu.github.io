import json, re, sys

slug = sys.argv[1]
body_file = sys.argv[2]
d = json.load(open('work/antiques/%s.json' % slug, encoding='utf-8'))
src = [it.get('zh') for it in d['items']]
body = open(body_file, encoding='utf-8').read()
blk = body.split("write('%s'" % slug)[1].split(']))')[0]
ens = re.findall(r'^\s*"(.*)",$', blk, re.M)
print('src=%d en=%d' % (len(src), len(ens)))
for i in range(max(len(src), len(ens))):
    s = src[i] if i < len(src) else '<<< NO SRC'
    e = ens[i] if i < len(ens) else '<<< NO EN'
    print('%3d | %-60s | %s' % (i, s[:60], e[:60]))
