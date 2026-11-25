import Syn.M1228
import Syn.M1360
import Syn.M1618
import Syn.M1905
import Syn.M1906

namespace Syn.M1937
def val : Nat := Syn.M1228.val % 7 + Syn.M1360.val % 7 + Syn.M1618.val % 7 + Syn.M1905.val % 7 + Syn.M1906.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1937
