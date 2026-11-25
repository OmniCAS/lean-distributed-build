import Syn.M1828
import Syn.M2172

namespace Syn.M2185
def val : Nat := Syn.M1828.val % 7 + Syn.M2172.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2185
