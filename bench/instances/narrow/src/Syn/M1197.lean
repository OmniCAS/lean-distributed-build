import Syn.M527
import Syn.M619
import Syn.M636
import Syn.M759
import Syn.M1102
import Syn.M1149

namespace Syn.M1197
def val : Nat := Syn.M527.val % 7 + Syn.M619.val % 7 + Syn.M636.val % 7 + Syn.M759.val % 7 + Syn.M1102.val % 7 + Syn.M1149.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1197
