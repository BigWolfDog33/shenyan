html="saklnk<p>djsakldj<"
print(html.find("<",7))
targ="<p>"
res=[]
x=html[6+len(targ):17]
res.append(x+'\\n')
res.append(x+'\\n')
print(res)
