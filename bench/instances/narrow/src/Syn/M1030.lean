import Syn.M12
import Syn.M18
import Syn.M444
import Syn.M498
import Syn.M500
import Syn.M558
import Syn.M962

namespace Syn.M1030
def val : Nat := Syn.M12.val % 7 + Syn.M18.val % 7 + Syn.M444.val % 7 + Syn.M498.val % 7 + Syn.M500.val % 7 + Syn.M558.val % 7 + Syn.M962.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1030
