import Syn.M705
import Syn.M709
import Syn.M827
import Syn.M1716

namespace Syn.M1729
def val : Nat := Syn.M705.val % 7 + Syn.M709.val % 7 + Syn.M827.val % 7 + Syn.M1716.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1729
