import Syn.M1286
import Syn.M1336
import Syn.M1630
import Syn.M1836

namespace Syn.M1858
def val : Nat := Syn.M1286.val % 7 + Syn.M1336.val % 7 + Syn.M1630.val % 7 + Syn.M1836.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1858
