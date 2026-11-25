import Syn.M1067
import Syn.M1830
import Syn.M1874
import Syn.M2309

namespace Syn.M2329
def val : Nat := Syn.M1067.val % 7 + Syn.M1830.val % 7 + Syn.M1874.val % 7 + Syn.M2309.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M2329
