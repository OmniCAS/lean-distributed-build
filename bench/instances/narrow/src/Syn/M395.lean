import Syn.M314

namespace Syn.M395
def val : Nat := Syn.M314.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M395
