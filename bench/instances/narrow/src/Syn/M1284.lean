import Syn.M52
import Syn.M162
import Syn.M245
import Syn.M384
import Syn.M459
import Syn.M611
import Syn.M636
import Syn.M664
import Syn.M667
import Syn.M712
import Syn.M800
import Syn.M917
import Syn.M1059
import Syn.M1157
import Syn.M1228

namespace Syn.M1284
def val : Nat := Syn.M52.val % 7 + Syn.M162.val % 7 + Syn.M245.val % 7 + Syn.M384.val % 7 + Syn.M459.val % 7 + Syn.M611.val % 7 + Syn.M636.val % 7 + Syn.M664.val % 7 + Syn.M667.val % 7 + Syn.M712.val % 7 + Syn.M800.val % 7 + Syn.M917.val % 7 + Syn.M1059.val % 7 + Syn.M1157.val % 7 + Syn.M1228.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1284
