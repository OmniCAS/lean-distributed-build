import Syn.M240
import Syn.M243
import Syn.M244
import Syn.M345
import Syn.M415
import Syn.M636
import Syn.M637
import Syn.M689
import Syn.M800
import Syn.M916
import Syn.M1119

namespace Syn.M1173
def val : Nat := Syn.M240.val % 7 + Syn.M243.val % 7 + Syn.M244.val % 7 + Syn.M345.val % 7 + Syn.M415.val % 7 + Syn.M636.val % 7 + Syn.M637.val % 7 + Syn.M689.val % 7 + Syn.M800.val % 7 + Syn.M916.val % 7 + Syn.M1119.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1173
