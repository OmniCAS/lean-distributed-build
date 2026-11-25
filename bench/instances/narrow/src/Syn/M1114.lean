import Syn.M713
import Syn.M833
import Syn.M930
import Syn.M939
import Syn.M971
import Syn.M1067

namespace Syn.M1114
def val : Nat := Syn.M713.val % 7 + Syn.M833.val % 7 + Syn.M930.val % 7 + Syn.M939.val % 7 + Syn.M971.val % 7 + Syn.M1067.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1114
