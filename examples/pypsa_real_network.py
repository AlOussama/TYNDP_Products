"""Optional adapter for a real pre-validated PyPSA netCDF.

Usage: python examples/pypsa_real_network.py my_grid.nc
Preflight intentionally rejects transformers/Links/storage until
explicit physical mappings are implemented. No silent component dropping.
"""
import sys
import pandas as pd
from tyndp_reduce.pypsa_adapter import require_pypsa,from_pypsa_network,aggregate_with_pypsa,injected_time_series
from tyndp_reduce.screening import method_a
from tyndp_reduce.clustering import greedy_busmap
from tyndp_reduce.aggregation import build_aggregation


def main(path):
    pypsa=require_pypsa()
    n=pypsa.Network(path)
    d=from_pypsa_network(n)
    p=injected_time_series(n)
    f,ranks=method_a(d,p)
    num_zones=max(2,len(d.bus_names)//5)
    zones=greedy_busmap(d,ranks.overload_MWh.to_numpy(),num_zones)
    agg=build_aggregation(d,zones)
    mapping={name:f'zone_{z}' for name,z in zip(d.bus_names,zones)}
    reduced,linemap=aggregate_with_pypsa(n,mapping)
    reduced.export_to_netcdf('reduced_unqualified.nc')
    pd.DataFrame({'bus':d.bus_names,'zone':zones}).to_csv('real_busmap.csv',index=False)
    print('Topological initialisation complete; calibrated x/c0/N-1 NOT YET attached to PyPSA network')

if __name__=='__main__':main(sys.argv[1])
