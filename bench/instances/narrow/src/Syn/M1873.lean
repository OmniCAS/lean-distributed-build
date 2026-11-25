import Syn.M244
import Syn.M662
import Syn.M1848

namespace Syn.M1873
def val : Nat := Syn.M244.val % 7 + Syn.M662.val % 7 + Syn.M1848.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1873
