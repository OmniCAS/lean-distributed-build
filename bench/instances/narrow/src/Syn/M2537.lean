import Syn.M1047
import Syn.M1593
import Syn.M1857
import Syn.M2349
import Syn.M2425
import Syn.M2432
import Syn.M2505
import Syn.M2506
import Syn.M2520
import Syn.M2522
import Syn.M2524
import Syn.M2525

namespace Syn.M2537
def val : Nat := Syn.M1047.val % 7 + Syn.M1593.val % 7 + Syn.M1857.val % 7 + Syn.M2349.val % 7 + Syn.M2425.val % 7 + Syn.M2432.val % 7 + Syn.M2505.val % 7 + Syn.M2506.val % 7 + Syn.M2520.val % 7 + Syn.M2522.val % 7 + Syn.M2524.val % 7 + Syn.M2525.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end Syn.M2537
