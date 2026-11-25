import Syn.M2515
import Syn.M2516
import Syn.M2517
import Syn.M2518
import Syn.M2519

namespace Syn.M2532
def val : Nat := Syn.M2515.val % 7 + Syn.M2516.val % 7 + Syn.M2517.val % 7 + Syn.M2518.val % 7 + Syn.M2519.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2532
