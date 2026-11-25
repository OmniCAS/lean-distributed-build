import Syn.M1966
import Syn.M1972

namespace Syn.M2027
def val : Nat := Syn.M1966.val % 7 + Syn.M1972.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2027
