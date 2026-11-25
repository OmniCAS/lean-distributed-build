import Syn.M48
import Syn.M125
import Syn.M128
import Syn.M131
import Syn.M132
import Syn.M135
import Syn.M214
import Syn.M215
import Syn.M216
import Syn.M217
import Syn.M218
import Syn.M339
import Syn.M340
import Syn.M412
import Syn.M473

namespace Syn.M540
def val : Nat := Syn.M48.val % 7 + Syn.M125.val % 7 + Syn.M128.val % 7 + Syn.M131.val % 7 + Syn.M132.val % 7 + Syn.M135.val % 7 + Syn.M214.val % 7 + Syn.M215.val % 7 + Syn.M216.val % 7 + Syn.M217.val % 7 + Syn.M218.val % 7 + Syn.M339.val % 7 + Syn.M340.val % 7 + Syn.M412.val % 7 + Syn.M473.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M540
