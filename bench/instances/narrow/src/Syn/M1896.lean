import Syn.M1148
import Syn.M1433
import Syn.M1798
import Syn.M1865

namespace Syn.M1896
def val : Nat := Syn.M1148.val % 7 + Syn.M1433.val % 7 + Syn.M1798.val % 7 + Syn.M1865.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1896
