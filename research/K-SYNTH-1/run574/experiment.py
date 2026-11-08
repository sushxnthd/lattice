import os, tempfile, pathlib, json
cases=[]
def record(name, condition, details):
    cases.append({'case':name,'passed':bool(condition),'details':details}); assert condition,name
with tempfile.TemporaryDirectory() as td:
    root=pathlib.Path(td); authorized=root/'authorized'; outside=root/'outside'; authorized.mkdir(); outside.mkdir()
    victim=outside/'victim.py'; victim.write_text('secret = 41\n')
    alias=authorized/'alias.py'; os.link(victim,alias)
    record('lexical_path_accepts_hardlink',alias.resolve().is_relative_to(authorized),{'alias':str(alias.relative_to(root)),'victim':str(victim.relative_to(root))})
    record('same_inode_and_nlink',os.stat(alias).st_ino==os.stat(victim).st_ino and os.stat(alias).st_nlink==2,{'inode':os.stat(alias).st_ino,'nlink':os.stat(alias).st_nlink})
    fd=os.open(alias,os.O_RDONLY|os.O_NOFOLLOW); read=os.read(fd,100); os.close(fd)
    record('nofollow_does_not_reject_hardlink',read==b'secret = 41\n',{'bytes':read.decode()})
    alias.write_text('secret = 99\n')
    record('inplace_edit_modifies_outside_inode',victim.read_text()=='secret = 99\n',{'outside_after':victim.read_text()})
    victim.write_text('secret = 41\n')
    staged=authorized/'staged.py'; staged.write_text('secret = 77\n'); os.replace(staged,alias)
    record('replace_breaks_hardlink_alias',victim.read_text()=='secret = 41\n' and alias.read_text()=='secret = 77\n',{'outside_after':victim.read_text(),'alias_after':alias.read_text()})
    record('nlink_guard_detects_but_not_proves_confinement',os.stat(victim).st_nlink==1 and os.stat(alias).st_nlink==1,{'scope':'POSIX local filesystem; nlink>1 is conservative rejection, nlink==1 does not prevent concurrent replacement or bind mounts'})
print(json.dumps({'experiment':'run574_hardlink_inplace_vs_replace','python':os.sys.version,'platform':os.uname().sysname,'cases':cases,'passed':sum(x['passed'] for x in cases),'total':len(cases)},indent=2))
