import Syn.M73

namespace Syn.M172
def val : Nat := Syn.M73.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M172
