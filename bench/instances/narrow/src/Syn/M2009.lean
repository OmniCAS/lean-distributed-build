import Syn.M1867
import Syn.M1868
import Syn.M1961

namespace Syn.M2009
def val : Nat := Syn.M1867.val % 7 + Syn.M1868.val % 7 + Syn.M1961.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2009
