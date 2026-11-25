import Syn.M1753
import Syn.M1771
import Syn.M1780
import Syn.M2134

namespace Syn.M2157
def val : Nat := Syn.M1753.val % 7 + Syn.M1771.val % 7 + Syn.M1780.val % 7 + Syn.M2134.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2157
