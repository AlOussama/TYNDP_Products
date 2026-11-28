"""C4 controls; never counted as frozen original paths."""
import sys,copy,unittest
from pathlib import Path
C3=Path(__file__).resolve().parents[1]/"BUNDLE_ML_04A_MS1_C3"
sys.path.insert(0,str(C3))
from run_originals import candidate_source
from original_record_binding import source_binding
from closure import Reject

class C4Controls(unittest.TestCase):
    def setUp(self):
        self.x,_,self.raw,_,_=candidate_source("RC02","B")
    def test_candidate_has_no_test_module_dependency(self):
        self.assertFalse({"test_closure","test_closure_v1"} & set(sys.modules))
    def test_original_source_binding(self):
        source_binding(self.x["definition"],self.x["instance"],self.raw)
    def test_reference_rename_rejected(self):
        x=copy.deepcopy(self.x)
        x["definition"]["reference"]="RENAMED"
        x["instance"]["record"]["id"]="RENAMED"
        with self.assertRaisesRegex(Reject,"ORIGINAL_REFERENCE_BINDING"):
            source_binding(x["definition"],x["instance"],self.raw)
    def test_source_bytes_rejected(self):
        with self.assertRaisesRegex(Reject,"ORIGINAL_SOURCE_BLOB"):
            source_binding(self.x["definition"],self.x["instance"],self.raw+b" ")
    def test_coordinate_tamper_rejected(self):
        x=copy.deepcopy(self.x)
        x["instance"]["raw_transfers"]["delivered"][0]="999"
        with self.assertRaisesRegex(Reject,"SOURCE_DATA_BINDING:delivered"):
            source_binding(x["definition"],x["instance"],self.raw)

if __name__=="__main__":unittest.main(verbosity=2)
