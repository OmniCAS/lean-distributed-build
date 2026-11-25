import Syn.M1145
import Syn.M1146
import Syn.M1797
import Syn.M1798
import Syn.M1815
import Syn.M1880
import Syn.M1881

namespace Syn.M1919
def val : Nat := Syn.M1145.val % 7 + Syn.M1146.val % 7 + Syn.M1797.val % 7 + Syn.M1798.val % 7 + Syn.M1815.val % 7 + Syn.M1880.val % 7 + Syn.M1881.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M1919
