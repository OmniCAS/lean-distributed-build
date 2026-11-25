import Syn.M1503
import Syn.M1663
import Syn.M1678
import Syn.M1939

namespace Syn.M1979
def val : Nat := Syn.M1503.val % 7 + Syn.M1663.val % 7 + Syn.M1678.val % 7 + Syn.M1939.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1979
