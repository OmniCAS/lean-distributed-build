import Syn.M1391
import Syn.M1463
import Syn.M2207

namespace Syn.M2228
def val : Nat := Syn.M1391.val % 7 + Syn.M1463.val % 7 + Syn.M2207.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2228
