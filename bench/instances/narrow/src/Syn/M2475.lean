import Syn.M2471

namespace Syn.M2475
def val : Nat := Syn.M2471.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2475
