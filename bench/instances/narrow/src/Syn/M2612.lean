import Syn.M2598
import Syn.M2602
import Syn.M2608
import Syn.M2611

namespace Syn.M2612
def val : Nat := Syn.M2598.val % 7 + Syn.M2602.val % 7 + Syn.M2608.val % 7 + Syn.M2611.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2612
