import E1.Formalism.CMTypeGalois.CMTypeFrobenius.HostConj
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.HostEmb
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.HostFrob
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.HostInertia
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.HostMu
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.KroneckerMeaning
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.MQFrob
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.MQGalois
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.MQKummer
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.TypesA
import E1.Formalism.CMTypeGalois.CMTypeFrobenius.TypesB

set_option Elab.async false

namespace E1N.M63
def val : Nat := E1N.M52.val % 7 + E1N.M53.val % 7 + E1N.M54.val % 7 + E1N.M55.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M63
