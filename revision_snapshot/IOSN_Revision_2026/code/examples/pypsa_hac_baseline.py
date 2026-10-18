"""Use PyPSA's prepared HAC baseline only, not congestion-aware optimisation.

This script illustrates direct PyPSA API reuse; scientific A/B clustering
needs the separate score-aware partition module and reference flow inputs.
"""
import sys
from tyndp_reduce.pypsa_adapter import require_pypsa

def run(path,zones):
    pypsa=require_pypsa();n=pypsa.Network(path)
    busmap=n.cluster.spatial.busmap_by_hac(n_clusters=zones)
    result=n.cluster.spatial.get_clustering_from_busmap(busmap,with_time=True)
    result.n.export_to_netcdf('hac_baseline_unqualified.nc')
    busmap.rename('zone').to_csv('hac_baseline_busmap.csv')
    print('HAC topology only; not congestion-aware, not TYNDP-calibrated')

if __name__=='__main__':run(sys.argv[1],int(sys.argv[2]))
