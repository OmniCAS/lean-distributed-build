import Syn.M12
import Syn.M444
import Syn.M916
import Syn.M1252
import Syn.M1343
import Syn.M1372

namespace Syn.M1413
def val : Nat := Syn.M12.val % 7 + Syn.M444.val % 7 + Syn.M916.val % 7 + Syn.M1252.val % 7 + Syn.M1343.val % 7 + Syn.M1372.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1413
