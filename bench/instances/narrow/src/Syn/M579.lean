import Syn.M109
import Syn.M201
import Syn.M202
import Syn.M203
import Syn.M204
import Syn.M465
import Syn.M534

namespace Syn.M579
def val : Nat := Syn.M109.val % 7 + Syn.M201.val % 7 + Syn.M202.val % 7 + Syn.M203.val % 7 + Syn.M204.val % 7 + Syn.M465.val % 7 + Syn.M534.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M579
