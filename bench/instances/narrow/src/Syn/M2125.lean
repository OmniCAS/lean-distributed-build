import Syn.M2095

namespace Syn.M2125
def val : Nat := Syn.M2095.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2125
