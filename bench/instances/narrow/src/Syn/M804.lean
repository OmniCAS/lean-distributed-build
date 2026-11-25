import Syn.M88
import Syn.M699

namespace Syn.M804
def val : Nat := Syn.M88.val % 7 + Syn.M699.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M804
