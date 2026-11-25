import Syn.M662
import Syn.M827
import Syn.M833
import Syn.M1929

namespace Syn.M1958
def val : Nat := Syn.M662.val % 7 + Syn.M827.val % 7 + Syn.M833.val % 7 + Syn.M1929.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1958
