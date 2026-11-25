import Syn.M744
import Syn.M1102
import Syn.M1184

namespace Syn.M1244
def val : Nat := Syn.M744.val % 7 + Syn.M1102.val % 7 + Syn.M1184.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1244
