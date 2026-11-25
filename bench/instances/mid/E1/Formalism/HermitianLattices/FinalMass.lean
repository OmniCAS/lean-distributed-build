import E1.Formalism.HermitianLattices.FinalNeighbourConstruct
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.MassBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.MassTelescope

set_option Elab.async false

namespace E1N.M702
def val : Nat := E1N.M703.val % 7 + E1N.M725.val % 7 + E1N.M726.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M702
