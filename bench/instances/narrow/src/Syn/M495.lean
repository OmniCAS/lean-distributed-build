import Syn.M429
import Syn.M430
import Syn.M442

namespace Syn.M495
def val : Nat := Syn.M429.val % 7 + Syn.M430.val % 7 + Syn.M442.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M495
