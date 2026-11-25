import Syn.M630
import Syn.M1004
import Syn.M1067
import Syn.M1115
import Syn.M1163
import Syn.M1822
import Syn.M1865

namespace Syn.M1894
def val : Nat := Syn.M630.val % 7 + Syn.M1004.val % 7 + Syn.M1067.val % 7 + Syn.M1115.val % 7 + Syn.M1163.val % 7 + Syn.M1822.val % 7 + Syn.M1865.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M1894
