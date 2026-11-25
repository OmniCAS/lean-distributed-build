import Syn.M598
import Syn.M1259

namespace Syn.M1312
def val : Nat := Syn.M598.val % 7 + Syn.M1259.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1312
