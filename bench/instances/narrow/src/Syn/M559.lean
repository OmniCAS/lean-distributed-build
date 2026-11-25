import Syn.M260
import Syn.M261
import Syn.M262
import Syn.M263
import Syn.M266
import Syn.M267
import Syn.M268
import Syn.M269
import Syn.M270
import Syn.M271
import Syn.M272
import Syn.M373
import Syn.M374
import Syn.M375
import Syn.M504

namespace Syn.M559
def val : Nat := Syn.M260.val % 7 + Syn.M261.val % 7 + Syn.M262.val % 7 + Syn.M263.val % 7 + Syn.M266.val % 7 + Syn.M267.val % 7 + Syn.M268.val % 7 + Syn.M269.val % 7 + Syn.M270.val % 7 + Syn.M271.val % 7 + Syn.M272.val % 7 + Syn.M373.val % 7 + Syn.M374.val % 7 + Syn.M375.val % 7 + Syn.M504.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M559
