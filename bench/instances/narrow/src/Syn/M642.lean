import Syn.M241
import Syn.M618
import Syn.M622

namespace Syn.M642
def val : Nat := Syn.M241.val % 7 + Syn.M618.val % 7 + Syn.M622.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M642
