"""Small deterministic candidate search; the editing AI makes the final semantic choice."""
import re

def search_effects(effects,query,stage=None,limit=3):
 q=query.lower();neg=re.findall(r'(?:不要|别用|不用|排除)([^，。；,;但]+)',q)
 positive=re.sub(r'(?:不要|别用|不用|排除)[^，。；,;但]+','',q)
 if not stage:
  choices={'opener':['开头','开场','片头'],'middle':['中间','中段','正文'],'closer':['结尾','收尾','谢幕','最后']}
  found=[k for k,terms in choices.items() if any(t in positive for t in terms)]
  if len(found)==1:stage=found[0]
 result=[]
 for e in effects:
  if stage and e['category']!=stage:continue
  excluded_terms=e.get('search_terms',[])+[e['name']]
  if any(len(t)>=2 and t.lower() in phrase for phrase in neg for t in excluded_terms):continue
  score=0;matched=[]
  for field,weight in [('use_cases',6),('styles',4),('search_terms',5),('aliases',2)]:
   for term in e.get(field,[]):
    t=term.lower()
    if len(t)>=2 and t in positive:
     score+=weight*min(len(t),5);matched.append(term)
  if score<=0:
   # Limited partial phrase matching, to find e.g. 培训回顾 inside a longer use case.
   for case in e.get('use_cases',[]):
    grams={case[i:i+2].lower() for i in range(len(case)-1)}
    hits=[g for g in grams if g in positive]
    if len(hits)>=2:score+=len(hits)*2;matched.extend(hits)
  if score>0:
   score+=2 if e['status']=='used' else -2 if e['status']=='idea' else 0
   result.append((e,score,list(dict.fromkeys(matched))))
 result.sort(key=lambda x:x[1],reverse=True)
 return result[:max(1,limit)]
