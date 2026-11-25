import Syn.M1463

namespace Syn.M1496
def val : Nat := Syn.M1463.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1496
