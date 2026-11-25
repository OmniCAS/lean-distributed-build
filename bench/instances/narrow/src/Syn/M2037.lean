import Syn.M1628
import Syn.M1979

namespace Syn.M2037
def val : Nat := Syn.M1628.val % 7 + Syn.M1979.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2037
