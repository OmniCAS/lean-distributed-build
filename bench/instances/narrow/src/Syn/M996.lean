import Syn.M637
import Syn.M804
import Syn.M805
import Syn.M920

namespace Syn.M996
def val : Nat := Syn.M637.val % 7 + Syn.M804.val % 7 + Syn.M805.val % 7 + Syn.M920.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M996
