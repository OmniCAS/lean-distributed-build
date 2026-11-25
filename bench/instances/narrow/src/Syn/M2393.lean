import Syn.M1151
import Syn.M1288
import Syn.M2293
import Syn.M2381

namespace Syn.M2393
def val : Nat := Syn.M1151.val % 7 + Syn.M1288.val % 7 + Syn.M2293.val % 7 + Syn.M2381.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2393
