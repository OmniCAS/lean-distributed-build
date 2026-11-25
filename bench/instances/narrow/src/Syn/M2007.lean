import Syn.M662
import Syn.M710
import Syn.M1929
import Syn.M1960

namespace Syn.M2007
def val : Nat := Syn.M662.val % 7 + Syn.M710.val % 7 + Syn.M1929.val % 7 + Syn.M1960.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2007
