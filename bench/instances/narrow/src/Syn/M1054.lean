import Syn.M772
import Syn.M773
import Syn.M775
import Syn.M985

namespace Syn.M1054
def val : Nat := Syn.M772.val % 7 + Syn.M773.val % 7 + Syn.M775.val % 7 + Syn.M985.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1054
