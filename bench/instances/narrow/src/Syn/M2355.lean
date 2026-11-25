import Syn.M1402
import Syn.M1810
import Syn.M1884
import Syn.M2221
import Syn.M2297
import Syn.M2302
import Syn.M2343

namespace Syn.M2355
def val : Nat := Syn.M1402.val % 7 + Syn.M1810.val % 7 + Syn.M1884.val % 7 + Syn.M2221.val % 7 + Syn.M2297.val % 7 + Syn.M2302.val % 7 + Syn.M2343.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2355
