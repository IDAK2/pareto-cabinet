import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as contract_actions
def calldata_compat(method=None,args=None,kwargs=None):
 out={}
 if method is not None: out['method']=method
 if args: out['args']=args
 if kwargs: out['kwargs']=kwargs
 return out
contract_actions.make_calldata_object=calldata_compat
ROOT=Path(__file__).parents[1]; ENV=(ROOT.parents[3]/'accounts.env').read_text(); ADDRESS=json.loads((ROOT/'deployment.json').read_text())['contractAddress']
def owner(): return create_account(account_private_key=re.search(r'^ACCOUNT_7_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip())
def wait(c,tx,expect='SUCCESS'):
 receipt=c.wait_for_transaction_receipt(transaction_hash=tx,wait_until='finalized',retries=180,interval=5000,full_transaction=True); leaders=receipt.get('consensus_data',{}).get('leader_receipt')or[]; leaders=[leaders] if isinstance(leaders,dict) else leaders; executions=[str(x.get('execution_result','')).upper() for x in leaders]; assert receipt.get('result_name')=='MAJORITY_AGREE' and expect in executions; return receipt,executions
def write(c,name,args,expect='SUCCESS'):
 tx=c.write_contract(address=ADDRESS,function_name=name,args=args); print(name+'_tx='+str(tx),flush=True); _,executions=wait(c,tx,expect); return str(tx),executions
curator=create_client(chain=studionet,account=owner()); submitters=[create_client(chain=studionet,account=create_account()) for _ in range(4)]; stamp=str(int(time.time())); aid='ASSAY-'+stamp; base='https://raw.githubusercontent.com/IDAK2/pareto-cabinet/main/fixtures/'; ids=['OFFLINE','ACCESS','RECOVERY']; descriptions=['Core reading and annotations remain usable without a continuous network connection.','Every primary operation has a keyboard path and meaningful screen-reader labels.','Interrupted work is saved locally and can be restored after a browser or device restart.']; tx={}; tx['open'],_=write(curator,'open_assay',[aid,'Resilient reading station',base+'brief.md',ids,descriptions]); observed=[]
for i,(key,label,file) in enumerate([('SLATE','Slate reader','slate.md'),('BEACON','Beacon reader','beacon.md'),('GLASS','Glass reader','glass.md')]):
 tx[key],_=write(submitters[i],'insert_candidate',[aid,key+'-'+stamp,label,base+file]); observed.append(curator.read_contract(address=ADDRESS,function_name='get_candidate',args=[key+'-'+stamp]))
before=curator.read_contract(address=ADDRESS,function_name='get_assay',args=[aid]); replay=submitters[3].write_contract(address=ADDRESS,function_name='insert_candidate',args=[aid,'COPY-'+stamp,'Copied slate',base+'slate.md']); tx['replay']=str(replay); replay_receipt,replay_execution=wait(submitters[3],replay,'ERROR'); after=curator.read_contract(address=ADDRESS,function_name='get_assay',args=[aid]); assert before==after; assert observed[0]['penalties']==[0,0,1] and observed[1]['penalties']==[1,0,0] and observed[2]['penalties']==[1,1,1]; assert observed[0]['status']=='FRONTIER' and observed[1]['status']=='FRONTIER' and observed[2]['status']=='DOMINATED'; tx['seal'],_=write(submitters[3],'seal_assay',[aid]); final=curator.read_contract(address=ADDRESS,function_name='get_assay',args=[aid]); assert final['state']=='SEALED' and len(final['frontier'])==2; proof={'assayId':aid,'contract':ADDRESS,'transactions':tx,'candidates':[{'id':x['id'],'penalties':x['penalties'],'status':x['status'],'artifactDigest':x['artifact_digest']} for x in observed],'final':final,'duplicateArtifact':{'consensus':replay_receipt.get('result_name'),'execution':replay_execution,'frontierUnchanged':before==after},'fixtureDisclosure':'The brief and candidate artifacts are operator-controlled public fixtures used to prove digest pinning, semantic vectors, dominance, replay rejection, and sealing.'}; (ROOT/'evidence').mkdir(exist_ok=True); (ROOT/'evidence'/'live-run.json').write_text(json.dumps(proof,indent=2)+'\n'); print(json.dumps(proof,indent=2))
