import Syn.M1755
import Syn.M1756
import Syn.M1757
import Syn.M1758
import Syn.M1759
import Syn.M1773

namespace Syn.M1785
def val : Nat := Syn.M1755.val % 7 + Syn.M1756.val % 7 + Syn.M1757.val % 7 + Syn.M1758.val % 7 + Syn.M1759.val % 7 + Syn.M1773.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1785
