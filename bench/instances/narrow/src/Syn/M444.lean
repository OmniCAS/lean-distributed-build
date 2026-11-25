import Syn.M170
import Syn.M171
import Syn.M172
import Syn.M173
import Syn.M175
import Syn.M249
import Syn.M252
import Syn.M253
import Syn.M254
import Syn.M365
import Syn.M370
import Syn.M371
import Syn.M372

namespace Syn.M444
def val : Nat := Syn.M170.val % 7 + Syn.M171.val % 7 + Syn.M172.val % 7 + Syn.M173.val % 7 + Syn.M175.val % 7 + Syn.M249.val % 7 + Syn.M252.val % 7 + Syn.M253.val % 7 + Syn.M254.val % 7 + Syn.M365.val % 7 + Syn.M370.val % 7 + Syn.M371.val % 7 + Syn.M372.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end Syn.M444
