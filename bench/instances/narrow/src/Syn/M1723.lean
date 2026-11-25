import Syn.M1713

namespace Syn.M1723
def val : Nat := Syn.M1713.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1723
