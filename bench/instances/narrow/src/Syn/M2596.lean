import Syn.M1581
import Syn.M1675
import Syn.M2590

namespace Syn.M2596
def val : Nat := Syn.M1581.val % 7 + Syn.M1675.val % 7 + Syn.M2590.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2596
