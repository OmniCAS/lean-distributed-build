import Syn.M744
import Syn.M2088
import Syn.M2217
import Syn.M2220

namespace Syn.M2243
def val : Nat := Syn.M744.val % 7 + Syn.M2088.val % 7 + Syn.M2217.val % 7 + Syn.M2220.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2243
