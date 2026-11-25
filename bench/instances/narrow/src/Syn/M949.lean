import Syn.M636
import Syn.M849

namespace Syn.M949
def val : Nat := Syn.M636.val % 7 + Syn.M849.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M949
