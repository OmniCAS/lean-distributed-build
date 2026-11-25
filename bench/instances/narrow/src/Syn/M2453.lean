import Syn.M1298
import Syn.M1924
import Syn.M1951
import Syn.M2270
import Syn.M2430
import Syn.M2439

namespace Syn.M2453
def val : Nat := Syn.M1298.val % 7 + Syn.M1924.val % 7 + Syn.M1951.val % 7 + Syn.M2270.val % 7 + Syn.M2430.val % 7 + Syn.M2439.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2453
