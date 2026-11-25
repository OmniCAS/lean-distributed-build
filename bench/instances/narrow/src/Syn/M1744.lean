import Syn.M1725

namespace Syn.M1744
def val : Nat := Syn.M1725.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1744
