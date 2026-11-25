import Syn.M12
import Syn.M444
import Syn.M497
import Syn.M500
import Syn.M962
import Syn.M1258

namespace Syn.M1307
def val : Nat := Syn.M12.val % 7 + Syn.M444.val % 7 + Syn.M497.val % 7 + Syn.M500.val % 7 + Syn.M962.val % 7 + Syn.M1258.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end Syn.M1307
