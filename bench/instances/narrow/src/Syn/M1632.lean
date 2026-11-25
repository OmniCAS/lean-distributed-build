import Syn.M878
import Syn.M1045
import Syn.M1607

namespace Syn.M1632
def val : Nat := Syn.M878.val % 7 + Syn.M1045.val % 7 + Syn.M1607.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1632
