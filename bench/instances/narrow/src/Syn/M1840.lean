import Syn.M743
import Syn.M1536
import Syn.M1816

namespace Syn.M1840
def val : Nat := Syn.M743.val % 7 + Syn.M1536.val % 7 + Syn.M1816.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1840
