"""Finite exact dimensional and monetary conversion controls; not an integrated operator extension."""
from dataclasses import dataclass
from fractions import Fraction as F
import re
from n1r import need, fields, digest, ident

@dataclass(frozen=True)
class Dimension:
    exponents: tuple
    @staticmethod
    def make(exponents):
        need(type(exponents) is dict and all(type(k) is str and type(v) is int for k,v in exponents.items()),'DIMENSION');return Dimension(tuple(sorted((k,v) for k,v in exponents.items() if v)))
    def combine(self,other,sign):
        d=dict(self.exponents)
        for k,v in other.exponents:d[k]=d.get(k,0)+sign*v
        return Dimension.make(d)

def basis(s):
    need(type(s) is str and re.fullmatch(r'[A-Z]{3}:(real|nominal):[0-9]{4}',s),'MONEY_BASIS');currency,kind,year=s.split(':');need(1900<=int(year)<=2300,'PRICE_YEAR');return currency,kind,int(year)

def monetary(value,src,dst,registry,rule_id,allowed_digest):
    """Explicit single-edge conversion. Registry trust is external and non-normative."""
    basis(src);basis(dst);need(digest(registry)==allowed_digest,'CONVERSION_REGISTRY_HASH');fields(registry,('schema','id','version','rules'));need(registry['schema']=='conversion-r1','CONVERSION_VERSION');ident(registry['id']);need(type(registry['version']) is str and registry['version'],'CONVERSION_VERSION');matches=[r for r in registry['rules'] if r['id']==rule_id];need(len(matches)==1,'CONVERSION_RULE');r=matches[0];fields(r,('id','from','to','factor','source_id','source_hash','authority'));need(r['from']==src and r['to']==dst and r['authority']=='RESEARCH_ASSUMPTION','CONVERSION_SCOPE');ident(r['source_id']);need(type(r['source_hash']) is str and re.fullmatch(r'[0-9a-f]{64}',r['source_hash']),'CONVERSION_SOURCE_HASH');need(type(r['factor']) is str and F(r['factor'])>0,'CONVERSION_FACTOR');need(type(value) in (str,int),'UNKNOWN_IS_NOT_ZERO');return {'value':str(F(value)*F(r['factor'])),'basis':dst,'rule':rule_id,'registry_digest':allowed_digest,'authority':'RESEARCH_ASSUMPTION','authenticity':'UNVERIFIED'}
