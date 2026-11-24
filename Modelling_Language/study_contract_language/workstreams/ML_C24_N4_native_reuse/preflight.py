import importlib.util,json,shutil,platform,subprocess
from pathlib import Path
r={'python':platform.python_version(),'mathspec_importable':importlib.util.find_spec('mathspec') is not None,'gems_executable':shutil.which('gems'),'sysml_executable':shutil.which('sysml'),'java':shutil.which('java'),'julia':shutil.which('julia')}
if r['java']:
    p=subprocess.run([r['java'],'-version'],capture_output=True,text=True);r['java_version']=p.stderr.strip()
r['native_status']={'mathspec':'NOT_EXECUTED','GEMS':'NOT_EXECUTED','SysML/KerML':'NOT_EXECUTED'}
print(json.dumps(r,indent=2))
