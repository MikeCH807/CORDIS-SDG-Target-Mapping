"""Offline release checks. No inference, network or private-master dependency."""
from pathlib import Path
import csv, json, hashlib, importlib.util, re, sys, math, collections, ast
import openpyxl
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(name,passed,detail=None):checks.append({'check':name,'passed':bool(passed),'detail':detail})
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rows(name):
 with (ROOT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def js(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def jl(name):return [json.loads(x) for x in (ROOT/name).read_text(encoding='utf-8-sig').splitlines() if x]
def index(seq,key):return {r[key]:r for r in seq}
EXPECTED={
 'data/cordis_sdg_mapping.csv':'1d33fdeb0604cb6e9dc70b10948550ff2953632b4841d9ccff6d87b1de710c76',
 'artifacts/final_responses.jsonl':'b42bc2ce73f4d7c465bb48b68bbabd3f9a3149316b20fb48ca214ed63e7d9756',
 'data/final_projects_150_privacy_clean.csv':'7075a9da63228019f0968b5d7060a4c1ac266ebe421150517f504a44d1a19e96',
 'artifacts/final_candidate_pairs_1500.csv':'6eab96127aacf69215b3acb33e205a15e3bc4883dc6ec241f6d7ad0c06a6a108',
 'data/CORDIS_SDG_Final_Mapping.xlsx':'1b600721efbd8988304e505d0ff0a9d3214f86abf1165e94634e0a10ff596821'}
for path,h in EXPECTED.items():check('protected_hash:'+path,sha(ROOT/path)==h)
for path,record in js('artifacts/copied_source_hashes.json').items():check('copied_hash:'+path,sha(ROOT/path)==record['sha256'])
m=rows('data/cordis_sdg_mapping.csv'); p=rows('data/project_mapping_summary.csv'); u=rows('data/uncertain_system_cases.csv'); c=rows('data/final_projects_150_privacy_clean.csv'); cand=rows('artifacts/final_candidate_pairs_1500.csv'); f=jl('artifacts/final_responses.jsonl'); e=jl('artifacts/final_project_evidence_150.jsonl')
M={x['project_id']+':'+x['target_code']:x for x in m}; C=index(c,'project_id'); E=index(e,'project_id'); F=index(f,'request_id'); CA=index(cand,'request_id')
n=[int(r['n_supported_mappings']) for r in p]
counts={'projects':len(p),'unique_projects':len({r['project_id'] for r in p}),'public_mappings':len(m),'mapped':sum(x>0 for x in n),'unmapped':sum(x==0 for x in n),'HIGH':sum(x['confidence_level']=='HIGH' for x in m),'MEDIUM':sum(x['confidence_level']=='MEDIUM' for x in m),'DIRECT':sum(x['contribution_type']=='DIRECT' for x in m),'INDIRECT':sum(x['contribution_type']=='INDIRECT' for x in m),'uncertain':len(u),'candidate_pairs':len(cand),'response_rows':len(f),'total_from_summary':sum(n),'mean_all':sum(n)/len(n),'mean_mapped':sum(n)/sum(x>0 for x in n),'max':max(n)}
check('counts',counts=={'projects':150,'unique_projects':150,'public_mappings':231,'mapped':100,'unmapped':50,'HIGH':88,'MEDIUM':143,'DIRECT':188,'INDIRECT':43,'uncertain':4,'candidate_pairs':1500,'response_rows':1500,'total_from_summary':231,'mean_all':1.54,'mean_mapped':2.31,'max':6},counts)
check('unique_mapping_keys',len(M)==len(m))
check('mapping_fields',all(x['match_strength'] in ['STRONG','WEAK'] and x['evidence'].strip() and x['explanation'].strip() and x['confidence_level']=={'STRONG':'HIGH','WEAK':'MEDIUM'}.get(x['match_strength']) and x['contribution_type'] in ['DIRECT','INDIRECT'] for x in m))
check('identity_populations',set(C)=={x['project_id'] for x in p}=={x['project_id'] for x in cand}==set(E) and len(CA)==len(cand)==len(F)==len(f)==1500 and set(CA)==set(F))
check('ten_unique_ranks_per_project',all(sorted(int(x['retrieval_rank']) for x in cand if x['project_id']==pid)==list(range(1,11)) for pid in C))
check('finite_retrieval_scores',all(math.isfinite(float(x['retrieval_score'])) for x in cand))
check('framework_diagnostic',collections.Counter(x['framework'] for x in c)=={'HORIZON_EUROPE':108,'OTHER':42} and sum(x['framework']=='OTHER' for x in m)==28 and sum(C[x['project_id']]['framework']=='OTHER' for x in cand)==420)
check('final_judgments',collections.Counter(x['final_result']['judgment'] if x['final_contract_valid'] else 'SYSTEM_INVALID' for x in f)=={'STRONG':88,'WEAK':143,'UNSUPPORTED':1265,'SYSTEM_INVALID':4})
check('public_exact_supported_set',set(M)=={x['request_id'] for x in f if x['final_contract_valid'] and x['final_result']['judgment'] in ['STRONG','WEAK']})
check('invalid_cases_separate', {x['request_id'] for x in u}=={x['request_id'] for x in f if not x['final_contract_valid']} and not(set(M)&{x['request_id'] for x in u}))
evidence_errors=[];lineage_errors=[]
for rid,r in M.items():
 seg=index(E[r['project_id']]['project_evidence_segments'],'id'); ids=[x.strip() for x in r['evidence_segment_ids'].split(';')];fr=F[rid]['final_result'];ca=CA[rid]
 if len(ids)!=len(set(ids)) or not ids or any(i not in seg for i in ids):evidence_errors.append(rid);continue
 reconstructed=' | '.join(' '.join(seg[i]['text'].split()) for i in ids)
 if r['evidence']!=reconstructed or any(C[r['project_id']][seg[i]['source']][seg[i]['start']:seg[i]['end']]!=seg[i]['text'] for i in ids):evidence_errors.append(rid)
 if (r['match_strength']!=fr['judgment'] or r['contribution_type']!=fr['contribution'] or r['explanation']!=fr['explanation'] or ids!=fr['evidence_segment_ids'] or r['target_wording']!=ca['target_wording'] or r['concept_uri']!=ca['concept_uri'] or r['retrieval_rank']!=ca['retrieval_rank'] or float(r['retrieval_score'])!=float(ca['retrieval_score'])):lineage_errors.append(rid)
check('all231_evidence_ownership_normalized_text',not evidence_errors,evidence_errors)
check('all231_lineage',not lineage_errors,lineage_errors)
summary_errors=[]
for r in p:
 subset=[x for x in m if x['project_id']==r['project_id']]
 if int(r['n_supported_mappings'])!=len(subset) or set(x.strip() for x in r['mapped_targets'].split(';') if x.strip())!={x['target_code'] for x in subset}:summary_errors.append(r['project_id'])
check('all150_project_summary',not summary_errors,summary_errors)
tax=rows('data/taxonomy_concepts.csv');T={x['code']:x for x in tax if 'http://metadata.un.org/sdg/ontology#Target' in x['types'].split('|')}
check('169_unique_targets',len(T)==169 and len({x['concept_uri'] for x in T.values()})==169)
check('all_candidate_target_references',all(x['target_code'] in T and x['concept_uri']==T[x['target_code']]['concept_uri'] and x['target_wording']==T[x['target_code']]['label'] for x in cand))
scope=index(jl('artifacts/scope_composition_inputs.jsonl'),'request_id');depth=index(jl('artifacts/depth_composition_inputs.jsonl'),'request_id')
spec=importlib.util.spec_from_file_location('frozen_composer',ROOT/'artifacts/frozen_verifier/compose_two_stage.py'); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
bad=[]
for rid,result in F.items():
 s=scope[rid];d=depth.get(rid,{})
 actual=mod.compose(rid,s['parsed_result'],s['contract_valid'],d.get('parsed_result'),d.get('contract_valid',False),{x['id'] for x in E[CA[rid]['project_id']]['project_evidence_segments']})
 if actual!=result:bad.append(rid)
check('all1500_deterministic_compositions',not bad,bad)
check('depth_only_valid_eligible_scope',set(depth)=={rid for rid,r in scope.items() if r['contract_valid'] and r['parsed_result']['eligibility']=='ELIGIBLE'} and len(depth)==234)
freeze=js('artifacts/freeze_manifest.json')
for key,name in {'composer_sha256':'compose_two_stage.py','scope_prompt_sha256':'scope_gate_prompt.txt','scope_schema_sha256':'scope_gate_schema.json','depth_prompt_sha256':'depth_grader_prompt.txt','depth_schema_sha256':'depth_grader_schema.json'}.items():check('verifier_hash:'+key,sha(ROOT/'artifacts/frozen_verifier'/name)==freeze[key])
w=openpyxl.load_workbook(ROOT/'data/CORDIS_SDG_Final_Mapping.xlsx',read_only=True,data_only=True)
def equal(a,b):
 if a is None:return b==''
 if isinstance(a,(int,float)):
  try:return math.isclose(float(a),float(b),rel_tol=1e-13,abs_tol=1e-15)
  except (ValueError,TypeError):return False
 return str(a)==b
for sheet,filename in [('Mappings','data/cordis_sdg_mapping.csv'),('Projects','data/project_mapping_summary.csv'),('Uncertain Cases','data/uncertain_system_cases.csv')]:
 with (ROOT/filename).open(encoding='utf-8-sig',newline='') as stream:raw=list(csv.reader(stream))
 values=list(w[sheet].values)
 mismatch=[i for i,(a,b) in enumerate(zip(values,raw)) if len(a)!=len(b) or not all(equal(x,y) for x,y in zip(a,b))]
 check('excel_csv:'+sheet,len(values)==len(raw) and not mismatch,{'rows_including_header':len(values),'mismatch_rows':mismatch})
check('excel_sheets',set(w.sheetnames)=={'Mappings','Projects','Uncertain Cases','QC Summary','QC Checks'})
check('excel_qc_checks',all(bool(v) for k,v in list(w['QC Checks'].values)[1:]))
w.close()
syntax=[];json_errors=[];paths=[];secrets=[];clutter=[]
for file in ROOT.rglob('*'):
 if not file.is_file() or '.git' in file.relative_to(ROOT).parts:continue
 rel=file.relative_to(ROOT).as_posix()
 if any(x in file.parts for x in ['__pycache__','.venv','.venv-holdout','.pytest_cache','.ipynb_checkpoints','history','models']) or file.name=='.env' or file.name.startswith('.env.') or file.suffix in ['.pyc','.log']:clutter.append(rel)
 if file.suffix not in ['.py','.md','.json','.jsonl','.csv','.txt','.toml','.ipynb']:continue
 text=file.read_text(encoding='utf-8-sig')
 if file.suffix=='.py':
  try:ast.parse(text)
  except SyntaxError:syntax.append(rel)
 if file.suffix in ['.json','.ipynb']:
  try:json.loads(text)
  except ValueError:json_errors.append(rel)
 if file.suffix=='.ipynb':
  nb=json.loads(text);text='\n'.join(''.join(c.get('source','')) for c in nb['cells'])+'\n'+'\n'.join(str(o.get('text','')) for c in nb['cells'] for o in c.get('outputs',[]))
 if re.search(r'[A-Za-z]:[\\/](?:Users|home)[\\/]|' + '/'+'Users'+'/'+'|'+'/'+'home'+r'/[^ /]+/',text):paths.append(rel)
 if re.search(r'\bsk-[A-Za-z0-9_-]{20,}\b|OPENAI_API_KEY\s*=\s*[\x22\x27]?[A-Za-z0-9_-]{12,}|\bBearer\s+[A-Za-z0-9_.-]{20,}',text):secrets.append(rel)
check('python_syntax',not syntax,syntax);check('json_validity',not json_errors,json_errors)
check('no_absolute_machine_paths',not paths,paths);check('no_likely_credentials',not secrets,secrets);check('no_private_clutter',not clutter,clutter)
app=(ROOT/'app/app.py').read_text(encoding='utf-8')
check('app_no_live_openai',not re.search(r'import\s+openai|from\s+openai|OpenAI\(|responses\.create\(|api\.openai\.com|chat\.completions',app))
nb=js('notebooks/final_analysis.ipynb');ids=[c.get('id','') for c in nb['cells']]
check('notebook_cell_ids',len(ids)==len(set(ids)) and all(re.fullmatch(r'[A-Za-z0-9_-]{1,64}',x) for x in ids))
if '--no-manifest' not in sys.argv:
 manifest_path=ROOT/'artifacts/release_manifest.json'
 if manifest_path.exists():
  manifest=js('artifacts/release_manifest.json');actual={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file() and p!=manifest_path and '.git' not in p.relative_to(ROOT).parts}
  check('release_manifest_inventory_and_hashes',actual==manifest['files'])
 else:check('release_manifest_present',False)
report={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'openai_api_calls':0,'reserve_semantic_access':False}
print(json.dumps(report,indent=2,ensure_ascii=True))
sys.exit(1 if report['failed'] else 0)
