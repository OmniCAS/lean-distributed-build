import Syn.M879
import Syn.M917

namespace Syn.M992
def val : Nat := Syn.M879.val % 7 + Syn.M917.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M992
