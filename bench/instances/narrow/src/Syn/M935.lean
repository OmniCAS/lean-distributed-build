import Syn.M160
import Syn.M234
import Syn.M433
import Syn.M636
import Syn.M638
import Syn.M641
import Syn.M832

namespace Syn.M935
def val : Nat := Syn.M160.val % 7 + Syn.M234.val % 7 + Syn.M433.val % 7 + Syn.M636.val % 7 + Syn.M638.val % 7 + Syn.M641.val % 7 + Syn.M832.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end Syn.M935
