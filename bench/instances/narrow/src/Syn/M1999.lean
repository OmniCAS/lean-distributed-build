import Syn.M1507
import Syn.M1947
import Syn.M1948

namespace Syn.M1999
def val : Nat := Syn.M1507.val % 7 + Syn.M1947.val % 7 + Syn.M1948.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1999
