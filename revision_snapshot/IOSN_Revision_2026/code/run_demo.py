"""Run standalone synthetic numerical demo without PyPSA."""
import argparse
from tyndp_reduce.demo import run_demo
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='outputs');p.add_argument('--seed',type=int,default=20261016)
    args=p.parse_args()
    df=run_demo(args.output,args.seed)
    print(df[['clustering','reference','validation_plain_RMSE_MW','validation_corrected_RMSE_MW','screening_coverage']].to_string(index=False))
