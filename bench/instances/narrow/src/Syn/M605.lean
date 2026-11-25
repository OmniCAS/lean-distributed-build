import Syn.M455
import Syn.M456
import Syn.M459
import Syn.M520
import Syn.M522
import Syn.M523
import Syn.M524
import Syn.M525
import Syn.M536
import Syn.M565
import Syn.M580
import Syn.M581
import Syn.M592

namespace Syn.M605
def val : Nat := Syn.M455.val % 7 + Syn.M456.val % 7 + Syn.M459.val % 7 + Syn.M520.val % 7 + Syn.M522.val % 7 + Syn.M523.val % 7 + Syn.M524.val % 7 + Syn.M525.val % 7 + Syn.M536.val % 7 + Syn.M565.val % 7 + Syn.M580.val % 7 + Syn.M581.val % 7 + Syn.M592.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end Syn.M605
