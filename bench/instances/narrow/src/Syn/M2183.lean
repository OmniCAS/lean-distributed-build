import Syn.M1727
import Syn.M1790
import Syn.M1836
import Syn.M1884
import Syn.M1947
import Syn.M2169

namespace Syn.M2183
def val : Nat := Syn.M1727.val % 7 + Syn.M1790.val % 7 + Syn.M1836.val % 7 + Syn.M1884.val % 7 + Syn.M1947.val % 7 + Syn.M2169.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2183
