import Syn.M636
import Syn.M637
import Syn.M689
import Syn.M800
import Syn.M916
import Syn.M1282

namespace Syn.M1328
def val : Nat := Syn.M636.val % 7 + Syn.M637.val % 7 + Syn.M689.val % 7 + Syn.M800.val % 7 + Syn.M916.val % 7 + Syn.M1282.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1328
