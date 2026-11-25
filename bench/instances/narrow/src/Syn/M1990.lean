import Syn.M960
import Syn.M1098
import Syn.M1184
import Syn.M1944
import Syn.M1945

namespace Syn.M1990
def val : Nat := Syn.M960.val % 7 + Syn.M1098.val % 7 + Syn.M1184.val % 7 + Syn.M1944.val % 7 + Syn.M1945.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1990
