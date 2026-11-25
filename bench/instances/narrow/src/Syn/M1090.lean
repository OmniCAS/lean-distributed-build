import Syn.M967
import Syn.M969
import Syn.M970
import Syn.M1037
import Syn.M1038
import Syn.M1039
import Syn.M1040

namespace Syn.M1090
def val : Nat := Syn.M967.val % 7 + Syn.M969.val % 7 + Syn.M970.val % 7 + Syn.M1037.val % 7 + Syn.M1038.val % 7 + Syn.M1039.val % 7 + Syn.M1040.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1090
