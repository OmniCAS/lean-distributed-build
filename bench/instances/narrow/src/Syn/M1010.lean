import Syn.M480
import Syn.M630
import Syn.M855
import Syn.M935

namespace Syn.M1010
def val : Nat := Syn.M480.val % 7 + Syn.M630.val % 7 + Syn.M855.val % 7 + Syn.M935.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1010
