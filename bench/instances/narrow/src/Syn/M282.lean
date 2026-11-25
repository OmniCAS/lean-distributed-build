import Syn.M181
import Syn.M182

namespace Syn.M282
def val : Nat := Syn.M181.val % 7 + Syn.M182.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M282
