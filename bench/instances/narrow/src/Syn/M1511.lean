import Syn.M38
import Syn.M1476

namespace Syn.M1511
def val : Nat := Syn.M38.val % 7 + Syn.M1476.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1511
