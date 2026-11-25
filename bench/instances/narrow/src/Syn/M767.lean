import Syn.M636
import Syn.M669

namespace Syn.M767
def val : Nat := Syn.M636.val % 7 + Syn.M669.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M767
