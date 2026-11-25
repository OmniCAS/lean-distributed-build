import Syn.M752
import Syn.M875
import Syn.M877
import Syn.M881

namespace Syn.M973
def val : Nat := Syn.M752.val % 7 + Syn.M875.val % 7 + Syn.M877.val % 7 + Syn.M881.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M973
