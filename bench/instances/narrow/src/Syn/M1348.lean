import Syn.M1114
import Syn.M1165
import Syn.M1311

namespace Syn.M1348
def val : Nat := Syn.M1114.val % 7 + Syn.M1165.val % 7 + Syn.M1311.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1348
