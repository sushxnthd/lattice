import json,unittest
import paired_repo_pilot as prior
import run218
import run217_matched_pilot as old

class Run218Tests(unittest.TestCase):
    def setUp(self):
        self.body=('def _featuresCompatible(designSpaceDoc):\n'
          '    """A long explanatory docstring that is not the intended edit."""\n'
          +''.join('    x = '+str(i)+'\n' for i in range(45))+
          '    return True\n')
        self.files={'Lib/ufo2ft/featureCompiler.py':self.body.encode()}
        self.issue={'instance_id':'test','problem_statement':'_featuresCompatible() incorrectly handles include statements'}
    def test_long_named_function_recall(self):
        f=run218.facts(self.files,self.issue)
        t=[x for x in f['Lib/ufo2ft/featureCompiler.py']['targets'] if x['name']=='_featuresCompatible']
        self.assertEqual(len(t),1)
        self.assertGreater(len(t[0]['old_text']),480)
    def test_lossless_presentation(self):
        f=run218.facts(self.files,self.issue)
        self.assertEqual(json.loads(json.dumps(f)),old.parse_python_view(old.python_view(f)))
    def test_shared_short_id_compiler(self):
        f=run218.facts(self.files,self.issue)
        path='Lib/ufo2ft/featureCompiler.py'
        t=next(t for t in f[path]['targets'] if t['name']=='_featuresCompatible')
        act={'op':'replace','path':path,'file_sha256':f[path]['file_sha256'],
             'selector':t['target_id'],'replacement':t['old_text'].replace('return True','return False'),'content':''}
        tx=prior.compile_arm(self.files,{'actions':[act]},set(self.files),'python_short_id')
        self.assertIn(b'return False',tx.changes[path])
    def test_fallback_without_named_identifier(self):
        f=run218.facts(self.files,{'problem_statement':'Repair compatibility checking.'})
        self.assertTrue(f['Lib/ufo2ft/featureCompiler.py']['targets'])
    def test_identical_output_schema(self):
        self.assertEqual(prior.response_format('python_short_id'),prior.response_format('python_text'))

if __name__=='__main__':unittest.main()
