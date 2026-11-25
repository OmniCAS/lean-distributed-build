import Syn.M25

namespace Syn.M99
def val : Nat := Syn.M25.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M99
