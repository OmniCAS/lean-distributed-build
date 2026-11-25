import Syn.M1509
import Syn.M1645

namespace Syn.M1663
def val : Nat := Syn.M1509.val % 7 + Syn.M1645.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1663
