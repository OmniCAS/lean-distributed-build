import Syn.M359
import Syn.M971
import Syn.M1526
import Syn.M2399

namespace Syn.M2412
def val : Nat := Syn.M359.val % 7 + Syn.M971.val % 7 + Syn.M1526.val % 7 + Syn.M2399.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M2412
