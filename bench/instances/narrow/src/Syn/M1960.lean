import Syn.M660
import Syn.M709
import Syn.M1286
import Syn.M1929

namespace Syn.M1960
def val : Nat := Syn.M660.val % 7 + Syn.M709.val % 7 + Syn.M1286.val % 7 + Syn.M1929.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1960
