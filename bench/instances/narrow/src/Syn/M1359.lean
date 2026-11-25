import Syn.M636
import Syn.M637
import Syn.M689
import Syn.M800
import Syn.M916
import Syn.M991
import Syn.M1172
import Syn.M1173
import Syn.M1328

namespace Syn.M1359
def val : Nat := Syn.M636.val % 7 + Syn.M637.val % 7 + Syn.M689.val % 7 + Syn.M800.val % 7 + Syn.M916.val % 7 + Syn.M991.val % 7 + Syn.M1172.val % 7 + Syn.M1173.val % 7 + Syn.M1328.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1359
