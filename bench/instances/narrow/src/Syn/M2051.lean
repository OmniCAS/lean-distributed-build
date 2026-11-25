import Syn.M1058
import Syn.M1988
import Syn.M1989
import Syn.M1990

namespace Syn.M2051
def val : Nat := Syn.M1058.val % 7 + Syn.M1988.val % 7 + Syn.M1989.val % 7 + Syn.M1990.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2051
