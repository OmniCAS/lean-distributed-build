import Syn.M2219

namespace Syn.M2239
def val : Nat := Syn.M2219.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2239
