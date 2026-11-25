import Syn.M2246
import Syn.M2262
import Syn.M2298
import Syn.M2322

namespace Syn.M2345
def val : Nat := Syn.M2246.val % 7 + Syn.M2262.val % 7 + Syn.M2298.val % 7 + Syn.M2322.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2345
