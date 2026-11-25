import Syn.M124
import Syn.M540
import Syn.M637
import Syn.M690
import Syn.M691
import Syn.M692
import Syn.M693
import Syn.M694
import Syn.M695
import Syn.M696
import Syn.M697
import Syn.M698
import Syn.M802
import Syn.M803
import Syn.M1111
import Syn.M1287

namespace Syn.M1333
def val : Nat := Syn.M124.val % 7 + Syn.M540.val % 7 + Syn.M637.val % 7 + Syn.M690.val % 7 + Syn.M691.val % 7 + Syn.M692.val % 7 + Syn.M693.val % 7 + Syn.M694.val % 7 + Syn.M695.val % 7 + Syn.M696.val % 7 + Syn.M697.val % 7 + Syn.M698.val % 7 + Syn.M802.val % 7 + Syn.M803.val % 7 + Syn.M1111.val % 7 + Syn.M1287.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1333
