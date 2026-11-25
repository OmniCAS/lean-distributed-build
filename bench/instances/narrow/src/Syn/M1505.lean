import Syn.M619
import Syn.M1469

namespace Syn.M1505
def val : Nat := Syn.M619.val % 7 + Syn.M1469.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1505
