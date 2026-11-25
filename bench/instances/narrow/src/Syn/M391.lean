import Syn.M38
import Syn.M101
import Syn.M102
import Syn.M103
import Syn.M104
import Syn.M105
import Syn.M106
import Syn.M107
import Syn.M108
import Syn.M196
import Syn.M197
import Syn.M198
import Syn.M292
import Syn.M293

namespace Syn.M391
def val : Nat := Syn.M38.val % 7 + Syn.M101.val % 7 + Syn.M102.val % 7 + Syn.M103.val % 7 + Syn.M104.val % 7 + Syn.M105.val % 7 + Syn.M106.val % 7 + Syn.M107.val % 7 + Syn.M108.val % 7 + Syn.M196.val % 7 + Syn.M197.val % 7 + Syn.M198.val % 7 + Syn.M292.val % 7 + Syn.M293.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M391
