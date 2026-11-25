import Syn.M360
import Syn.M361
import Syn.M662
import Syn.M835
import Syn.M929
import Syn.M1108
import Syn.M1286
import Syn.M1789
import Syn.M1801
import Syn.M1806
import Syn.M1847

namespace Syn.M1871
def val : Nat := Syn.M360.val % 7 + Syn.M361.val % 7 + Syn.M662.val % 7 + Syn.M835.val % 7 + Syn.M929.val % 7 + Syn.M1108.val % 7 + Syn.M1286.val % 7 + Syn.M1789.val % 7 + Syn.M1801.val % 7 + Syn.M1806.val % 7 + Syn.M1847.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1871
