import Syn.M1817
import Syn.M2128
import Syn.M2129

namespace Syn.M2149
def val : Nat := Syn.M1817.val % 7 + Syn.M2128.val % 7 + Syn.M2129.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2149
