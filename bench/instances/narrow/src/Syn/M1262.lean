import Syn.M662
import Syn.M1202

namespace Syn.M1262
def val : Nat := Syn.M662.val % 7 + Syn.M1202.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1262
