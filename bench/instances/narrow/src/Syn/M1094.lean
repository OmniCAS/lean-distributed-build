import Syn.M1048

namespace Syn.M1094
def val : Nat := Syn.M1048.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1094
