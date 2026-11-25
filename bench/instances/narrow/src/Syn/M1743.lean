import Syn.M743
import Syn.M1721
import Syn.M1724

namespace Syn.M1743
def val : Nat := Syn.M743.val % 7 + Syn.M1721.val % 7 + Syn.M1724.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1743
