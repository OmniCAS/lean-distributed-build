import Syn.M610
import Syn.M636

namespace Syn.M676
def val : Nat := Syn.M610.val % 7 + Syn.M636.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M676
