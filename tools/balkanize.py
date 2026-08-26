import os, re, glob, pathlib
vanilla_dir=r'C:\Program Files (x86)\Steam\steamapps\common\Hearts of Iron IV\history\states'
mod_dir=r'C:\Users\zendrix\Documents\Paradox Interactive\Hearts of Iron IV\mod\maratha-empire\history\states'
mapping={
423: ('RAJ',2),
424: ('RAJ',2),
425: ('MYS',4),
426: ('RAJ',2),
427: ('HYD',6),
428: ('WIS',3),
430: ('BAN',3),
431: ('BAN',4),
432: ('RAJ',2),
433: ('RJP',4),
434: ('RAJ',1),
435: ('RAJ',2),
436: ('CIP',3),
437: ('CIP',3),
438: ('RAJ',4),
439: ('RAJ',4),
440: ('PAK',3),
441: ('KAS',2),
442: ('PAK',2),
443: ('SIN',3),
982: ('RAJ',2),
984: ('CIP',2),
986: ('RAJ',2),
989: ('RJP',2),
990: ('RAJ',1),
991: ('RJP',3),
}
for sid,(owner,fabs) in mapping.items():
    fname=None
    for pat in [f'{sid}-*', f'{sid} -*', f'{sid}*']:
        m=glob.glob(os.path.join(vanilla_dir, pat))
        if m:
            fname=os.path.basename(m[0]); break
    if not fname:
        for f in os.listdir(vanilla_dir):
            if f.startswith(str(sid)):
                fname=f; break
    if not fname:
        print(f'not found {sid}')
        continue
    src=os.path.join(vanilla_dir, fname)
    txt=open(src,'r',encoding='utf-8',errors='ignore').read()
    txt=re.sub(r'owner\s*=\s*\w+', f'owner = {owner}', txt)
    if f'add_core_of = {owner}' not in txt:
        txt=txt.replace(f'owner = {owner}', f'owner = {owner}\n\t\tadd_core_of = {owner}',1)
    civ = max(1, fabs//2)
    mil = fabs - civ
    if 'industrial_complex' not in txt:
        txt=txt.replace('buildings = {', 'buildings = {\n\t\t\tindustrial_complex = '+str(civ)+'\n\t\t\tarms_factory = '+str(mil),1)
    else:
        # add extra if needed - just note
        pass
    dest=os.path.join(mod_dir, fname)
    open(dest,'w',encoding='utf-8').write(txt)
    print(f'wrote {fname} -> {owner} fabs {fabs}')
