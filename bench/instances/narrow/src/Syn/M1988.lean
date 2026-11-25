import Syn.M1879
import Syn.M1913
import Syn.M1914
import Syn.M1916
import Syn.M1945

namespace Syn.M1988
def val : Nat := Syn.M1879.val % 7 + Syn.M1913.val % 7 + Syn.M1914.val % 7 + Syn.M1916.val % 7 + Syn.M1945.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1988
