import Syn.M1217
import Syn.M1273
import Syn.M1601
import Syn.M1942

namespace Syn.M1987
def val : Nat := Syn.M1217.val % 7 + Syn.M1273.val % 7 + Syn.M1601.val % 7 + Syn.M1942.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M1987
