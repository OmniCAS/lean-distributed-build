import Syn.M1849
import Syn.M2031
import Syn.M2115
import Syn.M2179
import Syn.M2259

namespace Syn.M2293
def val : Nat := Syn.M1849.val % 7 + Syn.M2031.val % 7 + Syn.M2115.val % 7 + Syn.M2179.val % 7 + Syn.M2259.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2293
