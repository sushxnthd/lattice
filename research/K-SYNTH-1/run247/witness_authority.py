"""Executable authority-bypass witness for the earlier Run240/242 compiler.

Run after decoding the pinned Run240 runner into PYTHONPATH.
"""
import json
import run240

SOURCE='''class Service:
    def protected(self):
        return "ORIGINAL"

    def editable(self):
        return 1
'''
OLD='''    def editable(self):
        return 1
'''
EVIL='''    def editable(self):
        return 1

    def protected(self):
        return "OVERRIDDEN"
'''
PATH='service.py'
SELECTOR=run240.target_id(PATH,OLD)
FILES={PATH:SOURCE.encode()}
FACTS={'file_sha256':{PATH:run240.sha(FILES[PATH])},
       'blocks':[{'path':PATH,'name':'editable','kind':'method',
                  'authority':'editable','selector':SELECTOR,'code':OLD},
                 {'path':PATH,'name':'protected','kind':'method',
                  'authority':'read_only','selector':'a'*24,
                  'code':'    def protected(self):\n        return "ORIGINAL"\n'}]}
ACTION={'actions':[{'path':PATH,'file_sha256':FACTS['file_sha256'][PATH],
                    'selector':SELECTOR,'content':EVIL}]}

def run():
    original={};exec(SOURCE,original)
    after,traces=run240.compile_actions(FACTS,FILES,ACTION)
    modified={};exec(after[PATH],modified)
    before=original['Service']().protected()
    now=modified['Service']().protected()
    return {'compiler_accepted':True,'before':before,'after':now,
            'protected_changed':before!=now,'trace':traces,
            'patched_source_sha256':run240.sha(after[PATH])}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
